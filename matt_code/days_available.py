# 
# * To change this license header, choose License Headers in Project Properties.
# * To change this template file, choose Tools | Templates
# * and open the template in the editor.
# 
# *
# *
# * @author Matthew
# 
class DaysAvailable(object):
    def __init__(self, mon, tues, wed, thurs, fri, sat, sun):
        self.setMon(mon)
        self.setTues(tues)
        self.setWed(wed)
        self.setThurs(thurs)
        self.setFri(fri)
        self.setSat(sat)
        self.setSun(sun)

    def isMon(self):
        return self._mon

    def setMon(self, mon):
        self._mon = mon

    def isTues(self):
        return self._tues

    def setTues(self, tues):
        self._tues = tues

    def isWed(self):
        return self._wed

    def setWed(self, wed):
        self._wed = wed

    def isThurs(self):
        return self._thurs

    def setThurs(self, thurs):
        self._thurs = thurs

    def isFri(self):
        return self._fri

    def setFri(self, fri):
        self._fri = fri

    def isSat(self):
        return self._sat

    def setSat(self, sat):
        self._sat = sat

    def isSun(self):
        return self._sun

    def setSun(self, sun):
        self._sun = sun

    def isOnThatDay(self, dayNum):  # sunday is 0 and saturday is 6
        if dayNum == 0:
            return self.isSun()
        if dayNum == 1:
            return self.isMon()
        if dayNum == 2:
            return self.isTues()
        if dayNum == 3:
            return self.isWed()
        if dayNum == 4:
            return self.isThurs()
        if dayNum == 5:
            return self.isFri()
        if dayNum == 6:
            return self.isSat()
        return False

    def setDay(self, value, dayNum):
        if dayNum == 0:
            self.setSun(value)
        if dayNum == 1:
            self.setMon(value)
        if dayNum == 2:
            self.setTues(value)
        if dayNum == 3:
            self.setWed(value)
        if dayNum == 4:
            self.setThurs(value)
        if dayNum == 5:
            self.setFri(value)
        if dayNum == 6:
            self.setSat(value)

    def shareSameDay(self, block):
        if self.isMon() == block.isMon() or self.isTues() == block.isTues() or self.isWed() == block.isWed() or self.isThurs() == block.isThurs() or self.isFri() == block.isFri() or self.isSat() == block.isSat() or self.isSun() == block.isSun():
            return True
        return False

    def toString(self):
        days = ""
        if self.isMon():
            days = days + "Mo"
        if self.isTues():
            days = days + "Tu"
        if self.isWed():
            days = days + "We"
        if self.isThurs():
            days = days + "Th"
        if self.isFri():
            days = days + "Fr"
        if self.isSat():
            days = days + "Sa"
        if self.isSun():
            days = days + "Su"
        return days
