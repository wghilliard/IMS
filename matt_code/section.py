#
# * To change this license header, choose License Headers in Project Properties.
# * To change this template file, choose Tools | Templates
# * and open the template in the editor.
#
# *
# *
# * @author Matthew
#
class Section(object):
    Block = property()

    def __init__(self, sectionNum, startTime, endTime, days):
        self.super("class", "school", startTime, endTime, days)
        self.setSectionNum(sectionNum)

    def getSectionNum(self):
        return self._sectionNum

    def setSectionNum(self, sectionNum):
        if sectionNum == None:
            self._sectionNum = "TBA"
        else:
            self._sectionNum = sectionNum

    def toString(self):
        return "{sectionNumber: " + self.getSectionNum() + ", type: " + self.getType() + ", location: " + self.getLocation() + ", Time: " + self.getStartTime() + "-" + self.getEndTime() + " " + self.getDays() + "}"
