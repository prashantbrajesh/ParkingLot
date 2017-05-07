from backend.models.ParkingLot import ParkingLot
from BaseDao import BaseDao
from LogSetup import logging

class ParkingDao(BaseDao):

	def readRowFromTable(self, id):
		logging.info("ParkingDao read row")
		session = self.create_session()
		result = session.query(ParkingLot).filter_by(lotId = id).first()
		return result

	def updatetwoWheelerOccupied(self, id):
		logging.info("updatetwoWheelerOccupied update")
		session = self.create_session()
		result = session.query(ParkingLot).filter_by(lotId = id).first()
		result.twoWheelerOccupied = result.twoWheelerOccupied + 1
		session.commit()
		return result

	def updatelMVOccupied(self, id):
		logging.info("updatetwoWheelerOccupied update")
		session = self.create_session()
		result = session.query(ParkingLot).filter_by(lotId = id).first()
		result.lMVOccupied = result.lMVOccupied + 1
		session.commit()
		return result

	def updateRemovetwoWheelerOccupied(self, id):
		logging.info("updatetwoWheelerOccupied update")
		session = self.create_session()
		result = session.query(ParkingLot).filter_by(lotId = id).first()
		if(result.twoWheelerOccupied > 0):
			result.twoWheelerOccupied = result.twoWheelerOccupied - 1
		session.commit()
		return result

	def updateRemoveLmvOccupied(self, id):
		logging.info("updatetwoWheelerOccupied update")
		session = self.create_session()
		result = session.query(ParkingLot).filter_by(lotId = id).first()
		if(result.lMVOccupied > 0):
			result.lMVOccupied = result.lMVOccupied - 1
		session.commit()
		return result

def main():
	ObjCustCount = ParkingDao()
	# ObjCustCount.createTable()
	# ObjCustCount.insertIntoDb(0)
	# print json
	# ObjCustCount.deleteEntry()
	print ObjCustCount.readRowFromTable(2)
	# print ObjCustCount.getParking s()[0].eventTime

if __name__ == '__main__':
	main()
