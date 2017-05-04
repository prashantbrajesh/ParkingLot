from backend import app
from bottle import request, template, response
import simplejson as json
from backend.lib.LogSetup import logging
import sys, os
import thread
import ParkingConfig as config
from backend.models.Response import parkingResponse


@app.route("/ping", method='GET')
def ping():
	logging.debug("/ping GET called")
	return "ping";



@app.route('/test', method=['GET'])
def TestMode():
	from backend.controllers.TestModeController import TestModeController
	response.content_type = 'application/json'
	logging.info("Test mode API called")
	res = parkingResponse()
	try:
		if request.query.get("command"):
			if any(word in request.query.get("command") for word in ["start","stop","status","pause"]):
				logging.info("test command is %s"%request.query.get("command"))
				tbobj = TestModeController(request.query.get("command"))
				responsejson = tbobj.ProcessTestModeCommand()
				return responsejson
	except :
		logging.exception("Unable to process request failed")
	failure =  res.getFailureResponse()
	failure.status.message = "Unable to process request, command not valid"
	return failure.to_JSON()

