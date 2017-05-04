import json as json

class ParkingLot(object):

    def __init__(self, lotId, totalCountOfSpaces, twoWheelerParkingPrice, lMVParkingPrice,twoWheelerParkingCount):
        self.lotId = lotId # 1 for in and 0 for out
        self.totalCountOfSpaces = countOfSpaces
        self.twoWheelerParkingPrice = twoWheelerParkingPrice
        self.lMVParkingPrice = lMVParkingPrice
        self.twoWheelerParkingCount = twoWheelerParkingCount
        self.lMVParkingCount = totalCountOfSpaces - twoWheelerParkingCount
        self.twoWheelerOccupied = 0
        self.lMVOccupied = 0

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)