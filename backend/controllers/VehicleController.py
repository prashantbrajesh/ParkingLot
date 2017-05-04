from backend.lib.ManageParking import  addParkingLot, getParking, addVehicle
from backend.models.Response import parkingResponse
from backend.lib.LogSetup import logging


class VehicleController(object):

	def response_parking(self):
		res = parkingResponse()
		logging.info("response customer controller")
		try:
			data = getParking()
		except :
			logging.exception("Error Unable to get customers")
			failure =  res.getFailureResponse()
			failure.status.message = 'get Parking fail'
			return failure.to_JSON()

		success =  res.getSuccessResponse()
		if data:
			# for row in data:
			# 	time = datetime.fromtimestamp(row['eventTime'])
			# 	row['eventTime'] = str(time)

			logging.info("get Parking FFC %s"%data)
			success.response = data
		else:
			success.status.message = 'customer count empty'
			logging.info("get Parking FFC empty data: %s"%data)
		return success.to_JSON()

	def add_vehicle_at_lot(self,jsonData):
		res = parkingResponse()
		try:
			status = addVehicle(jsonData)
			if status:
				success =  res.getSuccessResponse()
				success.status.message = 'data posted successfully'
				return success.to_JSON()
		except :
			logging.exception("Unable to post parking lot to DB")

		failure =  res.getFailureResponse()
		failure.status.message = 'unable to post data'
		logging.info("parking lot post to DB of FFC failed")
		return failure.to_JSON()