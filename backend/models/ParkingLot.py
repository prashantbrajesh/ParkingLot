import json as json
from sqlalchemy import Column, Integer, String, Boolean
import sys
sys.path.append('/Users/braj/git/ParkingLots/')
print sys.path
from backend.lib.BaseDeclerative import Base

class ParkingLot(Base):
    __tablename__ = "parkinglot"
    lotId = Column(Integer, primary_key=True)  # 1 for in and 0 for out
    totalCountOfSpaces = Column(Integer,nullable=False)
    twoWheelerParkingPrice = Column(Integer,nullable=False)
    lMVParkingPrice = Column(Integer,nullable=False)
    twoWheelerParkingCount = Column(Integer,nullable=False)
    lMVParkingCount = Column(Integer,nullable=False)
    twoWheelerOccupied = Column(Integer,nullable=False)
    lMVOccupied = Column(Integer,nullable=False)

    def __init__(self, totalCountOfSpaces, twoWheelerParkingPrice, lMVParkingPrice,twoWheelerParkingCount):
        self.totalCountOfSpaces = totalCountOfSpaces
        self.twoWheelerParkingPrice = twoWheelerParkingPrice
        self.lMVParkingPrice = lMVParkingPrice
        self.twoWheelerParkingCount = twoWheelerParkingCount
        self.lMVParkingCount = totalCountOfSpaces - twoWheelerParkingCount
        self.twoWheelerOccupied = 0
        self.lMVOccupied = 0

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)