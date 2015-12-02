# 
# * To change this license header, choose License Headers in Project Properties.
# * To change this template file, choose Tools | Templates
# * and open the template in the editor.
# 
# *
# *
# * @author Matthew
#
from time import Time
from days_available import DaysAvailable


class Block(object):
    start_time = {
        "hours": None,
        "minutes": None
    }

    end_time = {
        "hours": None,
        "minutes": None
    }

    def __init__(self, classification, location, startTime, endTime, days):
        self.classification = classification
        self.location = location
        self.setStartTimeAndEndTime(startTime, endTime)
        self.setDays(days)

    def setStartTimeAndEndTime(self, startTime, endTime):

        if (endTime.getHours() == 0 and endTime.getMinutes() == 0) or startTime.lessThan(endTime):
            self._startTime = Time(startTime.getHours(), startTime.getMinutes())
            self._endTime = Time(endTime.getHours(), endTime.getMinutes())
        else:
            self._startTime = Time(0, 0)
            self._endTime = Time(0, 1)

    def setDays(self, days):
        if days == None:
            self._days = DaysAvailable(False, False, False, False, False, False, False)
        else:
            self._days = days

    def getDays(self):
        return self._days

    def getType(self):
        return self._type

    def getLocation(self):
        return self._location

    def getStartTime(self):
        return self._startTime

    def getEndTime(self):
        return self._endTime

    def checkNoConflicts(self, Block):
        pass
