from backend import app
from bottle import request, template, response
from backend.lib.LogSetup import logging
from backend.models.Response import parkingResponse
import simplejson as json

		
@app.route('/check', method=['GET'])
def headCountGet():
	from backend.controllers.CustomerController import CustomerController
	logging.debug("/headcount  GET called to post data to instore")
	cstHand = CustomerController()
	try:
		postJson = cstHand.post_to_instore()
		logging.debug('sending  %s'%(postJson))
	except ValueError:
		logging.exception("Some error occurred while trying to send headcount to instore")

	response.content_type = 'application/json'
	#post json response received from function is already serialized
	return postJson

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
			logging.info("The data posted is %s"%postJson)
			postResponse = cstHand.add_vehicle_at_lot(postJson)
			return postResponse
		except:
			logging.exception("Some error occurred while trying to create parking")

		res = parkingResponse()
		failure =  res.getFailureResponse()
		failure.status.message = 'Error during parking'
		return failure.to_JSON()


