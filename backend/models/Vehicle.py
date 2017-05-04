import json as json

class Vehicle(object):

    def __init__(self, lotId, vehicleType, vehicleId):
        self.lotId = lotId # 1 for in and 0 for out
        self.vehicleType = vehicleType
        self.VehicleId = vehicleId

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)