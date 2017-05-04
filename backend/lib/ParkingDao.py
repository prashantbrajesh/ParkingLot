import sqlite3
from sqlite3 import OperationalError
from threading import Lock
import os
# import sys
# sys.path.append('/Users/admin/parkinglot/ParkingLot/')
# print sys.path
import ParkingConfig as config

from LogSetup import logging
# from backend.models.ParkingLot import ParkingLot
MAXCOUNT = 922337203685477580
DB_FILE_PATH = os.path.join(config.DB_PATH, config.DB_NAME)



# logging.basicConfig(filename=config.LOG_PATH, format=config.LOG_FORMAT ,level=logging.DEBUG)
mutex = Lock()


class ParkingDao(object):
	idarray = []
	running_modes = {1:"live",0:"test"}
	TABLE_NAME = config.TABLE_NAME
	AUTO_INCRIMENT_TABLE  = config.AUTO_INCRIMENT_TABLE

	def __init__(self):

		try:
			self.conn = self.connectDb()
		except :
			logging.exception("DB connection Falied")
			raise


	def insertIntoDb(self, jsonData):
		logging.info("Inserting into db jsonData %s"%jsonData)

		try:
			self.conn = self.connectDb()
			c = self.conn.cursor()

			
			logging.info("Locking Index table to update")
			mutex.acquire()
			count = self.getIndex()
			logging.info("Current cout index is %d"%count)
			count = count + 1
			if (count >= MAXCOUNT):
				logging.info("MAX COUNT REACHED rolling back to 1")
				count = 1;
			self.updateIndex(count)

		except :
			logging.exception("Error update index db insert fail")
			raise
		finally:
			mutex.release()
			logging.info("Mutex released")

		logging.info("jsonData %s"%(jsonData))
		totalCountOfSpaces = jsonData["totalCountOfSpaces"]
		twoWheelerParkingPrice = jsonData["twoWheelerParkingPrice"]
		lMVParkingPrice = jsonData["lMVParkingPrice"]
		twoWheelerParkingCount = jsonData["twoWheelerParkingCount"]
		lMVParkingCount = jsonData["lMVParkingCount"]
		logging.info("count %d , jsonData %s"%(count,jsonData))
		sql = 'insert into '+ self.TABLE_NAME + ' (id ,time ,totalCountOfSpaces,twoWheelerParkingPrice,lMVParkingPrice,twoWheelerParkingCount,lMVParkingCount) values ( %d, strftime("%%s", "now"),%d,%d,%d,%d,%d)'%(count ,totalCountOfSpaces,twoWheelerParkingPrice,lMVParkingPrice,twoWheelerParkingCount,lMVParkingCount)
		

		# logging.info("Locking Index table to Insert Parking  Info")
		# mutex.acquire()
		try:
			c.execute(sql)
			self.conn.commit()
			self.conn.close()
			logging.info("Parking  inserted into db count %d "%(count))
		except OperationalError as e:
			logging.exception("no table exists, creating tables%s"%str(e))
			if "no such table" in str(e):
				self.createTable()
				self.insertIntoDb(jsonData)
		except  :
			logging.exception("Error in Inserting cust details in db ")

			

	def createTable(self):
		logging.info("Creating required tables")
		c = self.conn.cursor()

		sql = """create table if not exists %(table)s (
		ID INTEGER PRIMARY KEY ,
		totalCountOfSpaces INTEGER NOT NULL,
		twoWheelerParkingPrice INTEGER DEFAULT 0 ,
		lMVParkingPrice INTEGER DEFAULT 0 ,
		twoWheelerParkingCount INTEGER DEFAULT 0 ,
		lMVParkingCount INTEGER DEFAULT 0 ,
		twoWheelerOccupied INTEGER DEFAULT 0 ,
		lMVOccupied INTEGER DEFAULT 0 ,
		TIME INTEGER NOT NULL);"""%{'table':self.TABLE_NAME}

		sql1 = """create table if not exists %(table)s (
		indexvalue INTEGER DEFAULT 0,
		name varchar(15)
		);"""%{'table':self.AUTO_INCRIMENT_TABLE}

		try:
			c.execute(sql)
			c.execute(sql1)
			logging.info("Required Tables created")
		except  :
			logging.exception("Error Tables create fail ")


		sql = """insert into %(TableIndex)s ( indexvalue ,name) SELECT * FROM (SELECT 1, '%(Table)s') AS tmp
			WHERE NOT EXISTS (
			    SELECT name FROM %(TableIndex)s WHERE name = '%(Table)s'
			) LIMIT 1;"""%{"TableIndex": self.AUTO_INCRIMENT_TABLE,"Table":self.TABLE_NAME}
		# print sql
		try:
			c.execute(sql)
			self.conn.commit()
			logging.info("Tables initialization complete")
		except  :
			logging.exception("Error tables creation fail")



	def dropTable(self, table_name):
		logging.info("Droping Parking  table %s"%table_name)
		c = self.conn.cursor()
		sql =  'drop table ' + table_name
		try:
			c.execute(sql)
			self.updateIndex(1)
			logging.info("Parking  table deleted %s "%(sql))
		except  :
			logging.exception("Error unable to drop table Parking ")



	def getParkings(self):
		logging.info("Getting Parking details from DB")
		conn  = self.connectDb()
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		sql =  'select id ,time , totalCountOfSpaces,twoWheelerParkingPrice,lMVParkingPrice,twoWheelerParkingCount,lMVParkingCount , twoWheelerOccupied, lMVOccupied from ' + self.TABLE_NAME
		
		try:
			c.execute(sql)
			result_set = c.fetchall()
			Parking = {}
			idarray = []
			logging.info("cuetomer details from db fetched")
			i = 0
			for row in result_set:
				Parking[i] = {"totalCountOfSpaces" :row["totalCountOfSpaces"],"twoWheelerOccupied" :row["twoWheelerOccupied"],"lMVOccupied" :row["lMVOccupied"],"lMVParkingPrice" :row["lMVParkingPrice"]}
				
				i = i + 1
				idarray.append(row['ID'])

			# self.idarray = idarray
				logging.info("twoWheelerParkingPrice twoWheelerParkingPrice is : %d"%row['twoWheelerParkingPrice'])
			logging.info("Getting Parking details from DB done")
			return Parking
		except  :
			logging.exception("get Parking from db fail")



	def deleteEntry(self):
		logging.info("Deleting Parking details from DB")
		conn  = self.connectDb()
		c = conn.cursor()

		if  len(self.idarray) == 1:

			sql =  'delete from  %s where ID = %s ;'%(self.TABLE_NAME, self.idarray[0])
		else :
			sql =  'delete from  %s where ID in %s ;'%(self.TABLE_NAME, tuple(self.idarray))


		try:
			status = c.execute(sql)
			conn.commit()
			conn.close()
			logging.info("Id array Parking deleted are : %s"%self.idarray)
			self.idarray = []
			logging.info("Deleting Parking details from DB Done")
			return status
		except  :
			logging.exception("Deletion of customes data from DB fail")



	def getIndex(self):
		logging.info("Getting current index")
		conn  = self.connectDb()
		c = conn.cursor()
		sql =  'select indexvalue from %s where name = "%s"'%(self.AUTO_INCRIMENT_TABLE, self.TABLE_NAME)
		
		try:
			logging.info("%s"%sql)
			rows = c.execute(sql)
			count = rows.fetchone()
			logging.info("get index rows %s"%count)

			if count is None:
				self.createTable()
				return 1
			count = count[0]
			logging.info("Index value in auto increment table  : %d"%count)
			return int(count)

		except OperationalError as e:
			logging.exception("no table exists, creating tables %s"%str(e))
			if "no such table" in str(e):
				self.createTable()
				return 1
		except  :
			logging.exception("Unable to fetch current index of Parking ")


	def getRowParkingLot(self, lotId):
		logging.info("Getting current index")
		conn  = self.connectDb()
		c = conn.cursor()
		sql =  'select lMVOccupied, twoWheelerOccupied, twoWheelerParkingPrice, lMVParkingPrice from %s where id = %d'%(self.TABLE_NAME, lotId)
		
		try:
			logging.info("%s"%sql)
			rows = c.execute(sql)
			count = rows.fetchone()
			logging.info("get index rows %s"%type(count))
			# print count[0]

			if count is None:
				self.createTable()
				return 1
			
			# logging.info("Index value in auto increment table  : %d"%count)
			return count

		except OperationalError as e:
			logging.exception("no table exists, creating tables %s"%str(e))
			if "no such table" in str(e):
				self.createTable()
				return 1
		except  :
			logging.exception("Unable to fetch current index of Parking ")



	def updateParkingLot(self, vehicleType, lotId, inOrOut):
		logging.info("Updating current index")
		c = self.conn.cursor()
		# print count
		tuple_row = getRowParkingLot(lotId)
		if(tuple_row):
			lMVOccupied = tuple_row[0]
			twoWheelerOccupied = tuple_row[1]
			twoWheelerParkingPrice = tuple_row[2]
			lMVParkingPrice = tuple_row[3]
		sql3 =  'update %s set indexvalue = %d where name = "%s"'%( self.TABLE_NAME ,count ,self.TABLE_NAME)

		try:
			c.execute(sql3)
			logging.info("Index value updated to : %d for table %s "%(count,self.TABLE_NAME))
			self.conn.commit()
			
		except  :
			logging.exception("Index update failed")



	def connectDb(self):
		try:
			pass
			logging.info("Connecting to db")
			conn = sqlite3.connect(DB_FILE_PATH)

		except  :
			logging.exception("Unable to connect to DB %s"%DB_FILE_PATH)
			raise

		return conn



def main():
	ObjCustCount = ParkingDao()
	# ObjCustCount.createTable()
	# ObjCustCount.insertIntoDb(0)
	# print json
	# ObjCustCount.deleteEntry()
	print ObjCustCount.getRowParkingLot(2)
	# print ObjCustCount.getParking s()[0].eventTime

if __name__ == '__main__':
	main()
