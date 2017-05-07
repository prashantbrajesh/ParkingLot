from LogSetup import logging
from backend.models.Vehicle import Vehicle
from BaseDao import BaseDao


class VehicleDao(BaseDao):

    def readRowFromTable(self, id):
        logging.info("VehicleDao read row")
        session = self.create_session()
        result = session.query(Vehicle).filter_by(lotId = id).first()
        return result

    def getDetails(self, vid):
        logging.info("VehicleDao read row")
        session = self.create_session()
        result = session.query(Vehicle).filter_by(vehicleId = vid).first()
        return result


def main():
	ObjCustCount = VehicleDao()
	print ObjCustCount.readRowFromTable(1)
	# print ObjCustCount.getParking s()[0].eventTime

if __name__ == '__main__':
	main()
