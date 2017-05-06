import json as json
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer,String, Time
import sys
sys.path.append('/Users/braj/git/ParkingLots/')
print sys.path
from backend.lib.BaseDeclerative import Base


class Vehicle(Base):
    __tablename__ = "vehicle"
    lotId = Column(Integer, nullable = False)
    vehicleType = Column(String, nullable = False)
    VehicleId = Column(Integer, primary_key= True)
    time = Column(Time, onupdate=datetime.datetime.now())

    def __init__(self, lotId, vehicleType, vehicleId):
        self.lotId = lotId
        self.vehicleType = vehicleType
        self.VehicleId = vehicleId

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)