#!/usr/bin/python
import os, sys
from backend import app
from bottle import run, debug, request, response
from backend.lib.LogSetup import logging
import ParkingConfig as config
sys.path.append('/Users/admin/parkinglot/ParkingLot')
PORT = config.API_SERVER_PORT


def FreePort():
	if 'skip' not in sys.argv:
		logging.info("Trying to Kill process on port %s"%PORT)
		try:
			os.popen("kill -9 $(lsof -i :8081 | grep 'Python' | awk '{print $2}' )")
			pass
		except :
			logging.exception('Unable to free the port')

def main():
	logging.debug("Inside Main Run Api Server. Trying to start the API server")
		#port = int(os.environ.get("PORT", PORT))
	try:
		run(app, host='0.0.0.0', port=PORT, reloader=True)

	except:
		logging.exception("An error occurred while trying to start the API server")
		#FreePort()
		#main()




if __name__ == '__main__':
	main()