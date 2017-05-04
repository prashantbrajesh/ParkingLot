#!/usr/bin/python
import json as json

class statusFfc(object):

    success = True
    code = 200
    message = "success"

    def getSuccessStatus(self):
        self.code = 200
        self.message = "success"
        self.success = True
        return self;

    def getFailureStatus(self):
        self.code = 500
        self.success = False
        self.message = "failure"
        return self;

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
