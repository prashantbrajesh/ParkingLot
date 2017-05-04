import sys, os
from backend import app
from bottle import static_file
from backend.models.Response import parkingResponse
import ParkingConfig as config
from backend.lib.LogSetup import logging


# @app.route('/image')
# def favicon():
# 	logging.debug("/image  GET ")
# 	try:
# 		if ( Commands.capture() == True ):
# 			logging.debug("Image captured successful. Sending Image.")
# 			return static_file(config.IMAGE_FILENAME, root=config.IMAGE_LOC)
# 	except:
# 		logging.exception("capture image failed")
# 		message = "capture image failed"
# 	logging.debug("Error getting Image")
# 	res = parkingResponse()
# 	failure =  res.getFailureResponse()
# 	if not message:
# 		failure.status.message = 'Error getting Image'
# 	return failure.to_JSON()


