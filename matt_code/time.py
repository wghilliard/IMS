# 
# * To change this license header, choose License Headers in Project Properties.
# * To change this template file, choose Tools | Templates
# * and open the template in the editor.
# 
# *
# *
# * @author Matthew
# 
class Time(object):
    def __init__(self, hours, minutes):
        self.setHours(hours)
        self.setMinutes(minutes)

    def setHours(self, hours):
        if hours >= 0 and hours < 24:
            self._hours = hours
        else:
            self._hours = 0

    def setMinutes(self, minutes):
        if minutes >= 0 and minutes < 60:
            self._minutes = minutes
        else:
            self._minutes = 0

    # public void addMinutes(int minutes)
    # {
    # int totalMinutes = minutes + this.minutes;
    # if(totalMinutes/60!=0)
    # {
    # setMinutes(totalMinutes%60);
    # int totalHours = totalMinutes/60 + this.hours;
    # setHours(totalHours%24);
    # }
    # else
    # setMinutes(totalMinutes);
    # }
    def lessThan(self, Time):
        pass
