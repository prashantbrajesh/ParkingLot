from backend import app
from bottle import request, template, response
from backend.lib.LogSetup import logging
import backend.lib.ManageParking as  mngParking
from backend.models.Response import parkingResponse
import simplejson as json
import datetime

@app.route('/parkings', method=['GET'])
def getRecentCustomers():
	from backend.controllers.ParkingController import ParkingController
	logging.debug("/parkings  GET called")
	cstHand = ParkingController()
	try:
		postJson = cstHand.response_parking()
		logging.debug('sending  %s'%(postJson))
	except ValueError:
		logging.exception("Some error occurred while trying to get customer count")

	response.content_type = 'application/json'
	#post json response received from function is already serialized
	return postJson


@app.route("/parkinglot/add", method='POST')
def addParkingLot():
	if request.method == 'POST':
		from backend.models.Response import parkingResponse
		#removed logging from this function as it is the primary call and will be logged a lot of times
		response.content_type = 'application/json'
		from backend.controllers.ParkingController import ParkingController
		cstHand = ParkingController()
		try:
			postJson = json.load(request.body)
			logging.info("The data posted is %s"%postJson)
			postResponse = cstHand.add_parking_lot(postJson)
			return postResponse
		except:
			logging.exception("Some error occurred while trying to create parking lot")

		res = parkingResponse()
		failure =  res.getFailureResponse()
		failure.status.message = 'Error during creating parking lot'
		return failure.to_JSON()


@app.route("/vehicle/park", method='POST')
def addVehicle():
	if request.method == 'POST':
		from backend.models.Response import parkingResponse
		#removed logging from this function as it is the primary call and will be logged a lot of times
		response.content_type = 'application/json'
		from backend.controllers.VehicleController import VehicleController
		cstHand = VehicleController()
		try:

			postJson = json.load(request.body)
			obj = mngParking.getParkingDetaisByLotId(postJson["lotId"])
			logging.info("here i amj")
			logging.info(obj)
			if (postJson["vehicleType"] == "two"):
				if (obj["twoWheelerParkingCount"] - obj["twoWheelerOccupied"]) > 0:
					mngParking.updateParkingLot("two", postJson["lotId"])
			if (postJson["vehicleType"] == "lmv"):
				if (obj["lMVParkingCount"] - obj["lMVOccupied"]) > 0:
					mngParking.updateParkingLot("lmv", postJson["lotId"])
			logging.info("The data posted is %s"%postJson)
			postResponse = cstHand.add_vehicle_at_lot(postJson)
			return postResponse
		except:
			logging.exception("Some error occurred while trying to create parking")

		res = parkingResponse()
		failure =  res.getFailureResponse()
		failure.status.message = 'Error during parking'
		return failure.to_JSON()


@app.route("/vehicle/remove", method='GET')
def removeVehicle():
	if request.method == 'GET':
		from backend.models.Response import parkingResponse
		logging.info("remove")
		#removed logging from this function as it is the primary call and will be logged a lot of times
		response.content_type = 'application/json'
		vehicleId = request.query.get("vehicleid")
		try:
			logging.info("v id is %s"%vehicleId)
			obj = mngParking.getVechileDetaisl(vehicleId)
			logging.info(obj)
			objLot = mngParking.getParkingDetaisByLotId(obj.lotId)
			 
			logging.info(obj)
			if (obj.vehicleType == "two"):
				rate = objLot["twoWheelerParkingPrice"]
				mngParking.updateRemoveParkingLot("two", obj.lotId)
			if (obj.vehicleType == "lmv"):
				rate = objLot["lMVParkingPrice"]
				mngParking.updateRemoveParkingLot("lmv", obj.lotId)

			TimeStart = obj.insert_time
			now = datetime.datetime.now()
			logging.info(TimeStart)
			logging.info((now - TimeStart ).total_seconds())
			delatTime = (now - TimeStart ).total_seconds()
			logging.info(rate)
			return {"cost": (int)(delatTime/(60*60))*rate,"vehicleid":vehicleId,"duration": (delatTime)/(60*60)}
		except:
			logging.exception("Some error occurred while trying to create parking")

		res = parkingResponse()
		failure =  res.getFailureResponse()
		failure.status.message = 'Error during removing'
		return failure.to_JSON()
