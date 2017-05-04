#!/usr/bin/python
from ParkingDao import ParkingDao
from VehicleDao import VehicleDao
import requests, os, sys
import json
import ParkingConfig as config
from LogSetup import logging





def getParking():
	logging.info("get Parking Manage head count")
	try:
		pDao = ParkingDao()
		# cust.createTable()
		postJson = pDao.getParkings()
		return postJson
	except :
		logging.exception("Get Parking Info failed")
		raise

def deleteTables(type="_Test"):
	logging.info("Deleting the customer tables")
	try:
		pDao = ParkingDao()
		pDao.dropTable(config.TABLE_NAME+type)
	except :
		logging.exception("Parking Table delete failed")
		raise

def addParkingLot(jsonData):
	try:
		pDao = ParkingDao()
		# cust.createTable()
		pDao.insertIntoDb(jsonData)
		return True
	except:
		logging.exception("Some error occurred while trying to insert in/out in DB")
		return False


def addVehicle(jsonData):
	try:
		pDao = VehicleDao()
		# cust.createTable()
		pDao.insertIntoDb(jsonData)
		return True
	except:
		logging.exception("Some error occurred while trying to insert in/out in DB")
		return False

