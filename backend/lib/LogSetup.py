import logging
from logging.handlers import RotatingFileHandler
import ParkingConfig as Config

def getLogger():
	log_formatter = logging.Formatter(Config.LOG_FORMAT)
	logFile = Config.LOG_PATH

	my_handler = RotatingFileHandler(logFile, mode='a', maxBytes=50*1024*1024,
									 backupCount=6, encoding=None, delay=0)
	my_handler.setFormatter(log_formatter)
	my_handler.setLevel(logging.DEBUG)


	app_log = logging.getLogger('storeLogger')
	app_log.setLevel(logging.DEBUG)
	app_log.propagate = False

	if not app_log.handlers:
		app_log.addHandler(my_handler)

	return app_log

logging = getLogger()