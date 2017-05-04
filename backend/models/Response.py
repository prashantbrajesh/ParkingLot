#!/usr/bin/python
from StatusFfc import statusFfc
import json as json

class parkingResponse(object):

    def __init__(self):
        self.status = statusFfc()
        self.response = None

    def getSuccessResponse(self):        
        self.status = self.status.getSuccessStatus()
        self.response = None
        return self

    def getFailureResponse(self):
        self.status = self.status.getFailureStatus()
        self.response = None
        return self

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
