#!/usr/bin/python
from ParkingDao import ParkingDao
from VehicleDao import VehicleDao
import requests, os, sys
import json
import ParkingConfig as config
from LogSetup import logging
from backend.models.ParkingLot import ParkingLot
from backend.models.Vehicle import Vehicle





def getParking():
	logging.info("get Parking Manage head count")
	try:
		pDao = ParkingDao()
		# cust.createTable()
		postJson = pDao.readRowFromTable(1)
		postJson.__dict__["_sa_instance_state"] = ""
		logging.info(postJson.__dict__)
		return postJson.__dict__
	except :
		logging.exception("Get Parking Info failed")
		raise

def getParkingDetaisByLotId(id):
	logging.info("get Parking Manage head count")
	try:
		pDao = ParkingDao()
		# cust.createTable()
		postJson = pDao.readRowFromTable(id)
		postJson.__dict__["_sa_instance_state"] = ""
		logging.info(postJson.__dict__)
		return postJson.__dict__
	except :
		logging.exception("Get Parking Info failed")
		raise

def addParkingLot(jsonData):
	try:
		totalCountOfSpaces = jsonData["totalCountOfSpaces"]
		twoWheelerParkingPrice = jsonData["twoWheelerParkingPrice"]
		lMVParkingPrice = jsonData["lMVParkingPrice"]
		twoWheelerParkingCount = jsonData["twoWheelerParkingCount"]
		parkingLotObj = ParkingLot(totalCountOfSpaces, twoWheelerParkingPrice, lMVParkingPrice,twoWheelerParkingCount)
		pDao = ParkingDao()
		pDao.insertIntoTable(parkingLotObj)
		return True
	except:
		logging.exception("Some error occurred while trying to insert in/out in DB")
		return False


def addVehicle(jsonData):
	try:
		lotId = jsonData["lotId"]
		vehicleType = jsonData["vehicleType"]
		vehicleId = jsonData["vehicleId"]
		vachileObj = Vehicle(vehicleType, vehicleId)
		pDao = VehicleDao()
		# cust.createTable()
		pDao.insertIntoTable(vachileObj)
		return True
	except:
		logging.exception("Some error occurred while trying to insert in/out in DB")
		return False

