import json as json
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String, Time, ForeignKey, DateTime
import sys
sys.path.append('/Users/braj/git/ParkingLots/')
print sys.path
from backend.lib.BaseDeclerative import Base
from ParkingLot import ParkingLot


class Vehicle(Base):
    __tablename__ = "vehicle"
    lotId = Column(Integer, ForeignKey(ParkingLot.lotId), nullable = False)
    id = Column(Integer, primary_key=True)
    vehicleType = Column(String, nullable = False)
    vehicleId = Column(Integer, unique= True)
    insert_time = Column(DateTime)

    def __init__(self, lotId, vehicleType, vehicleId):
        self.lotId = lotId
        self.vehicleType = vehicleType
        self.vehicleId = vehicleId
        self.insert_time = datetime.datetime.now()

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)