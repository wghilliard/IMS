# *
# *
# * @author Matthew
#
class User(object):
    def __init__(self, workToSchool, homeToSchool, workToHome, sleepHours, sleepMinutes, studyHours, studyMinutes):
        # self._schedules = []
        # self._fetchedSections = ArrayList[ArrayList]()
        self._blockOuts = []
        self._courses = ArrayList[str]()
        self._email = "dogTeam"
        self._password = "yeah"
        self.setWorkToSchool(workToSchool)
        self.setHomeToSchool(homeToSchool)
        self.setWorkToHome(workToHome)
        self.setSleepHours(sleepHours)
        self.setSleepMinutes(sleepMinutes)
        self.setStudyHours(studyHours)
        self.setStudyMinutes(studyMinutes)

    def getStudyHours(self):
        return self._studyHours

    def setStudyHours(self, studyHours):
        if studyHours >= 0:
            self._studyHours = studyHours
        else:
            self._studyHours = 0

    def getStudyMinutes(self):
        return self._studyMinutes

    def setStudyMinutes(self, studyMinutes):
        if studyMinutes >= 0:
            self._studyMinutes = studyMinutes
        else:
            self._studyMinutes = 0

    def setWorkToSchool(self, workToSchool):
        if workToSchool >= 0 and workToSchool < 24 * 60:
            self._workToSchool = workToSchool
        else:
            self._workToSchool = 0

    def setHomeToSchool(self, homeToSchool):
        if homeToSchool >= 0 and homeToSchool < 24 * 60:
            self._homeToSchool = homeToSchool
        else:
            self._homeToSchool = 0

    def setWorkToHome(self, workToHome):
        if workToHome >= 0 and workToHome < 24 * 60:
            self._workToHome = workToHome
        else:
            self._workToHome = 0

    def setNotification(self, notification):
        self._notification = notification

    def getSleepHours(self):
        return self._sleepHours

    def setSleepHours(self, sleepHours):
        if sleepHours >= 6 and sleepHours <= 24:
            self._sleepHours = sleepHours
        else:
            self._sleepHours = 6

    def getSleepMinutes(self):
        return self._sleepMinutes

    def setSleepMinutes(self, sleepMinutes):
        if self._sleepHours == 24:
            self._sleepMinutes = 0
        elif sleepMinutes >= 0 and sleepMinutes < 60:
            self._sleepMinutes = sleepMinutes
        else:
            self._sleepMinutes = 0

    def makeSleepBlock(self):
        daysAvailable = DaysAvailable(True, True, True, True, True, True, True)
        self._sleepBlock = Block("sleep", "home", Time(0, 0), Time(self.getSleepHours(), self.getSleepMinutes()),
                                 daysAvailable)
        valid = self.addBlockOut(self._sleepBlock)
        if not valid:
            self.setNotification("No room for mandatory sleep!")
            return False
        return True

    def getWorkToSchool(self):
        return self._workToSchool

    def getHomeToSchool(self):
        return self._homeToSchool

    def getWorkToHome(self):
        return self._workToHome

    def getNotification(self):
        return self._notification

    def addCourse(self, course):
        i = 0
        while i < self._courses.size():
            if self._courses.get(i).compareTo(course) == 0:
                self.setNotification("Course was not added becuase it matched one" + " of your existing courses.")
                return False
            i += 1
        self._courses.add(course)
        self.setNotification("Course is successfully added.")
        return True

    def addBlockOut(self, blockOut):
        self.setNotification("")
        valid = True
        i = 0
        while i < self._blockOuts.size():
            if not (blockOut.checkNoConflicts(self._blockOuts.get(i))):
                self.setNotification("BlockOut conflicted with other blockOuts")
                valid = False
            i += 1
        if not valid:
            return False
        self._blockOuts.add(blockOut)
        self.setNotification("BlockOut was successfully added")
        return True

    def printCourses(self):
        if self._courses.size() == 0:
            Console.WriteLine("No courses available")
            return
        Console.WriteLine("Courses:")
        i = 0
        while i < self._courses.size():
            Console.WriteLine("\tCourse " + i + ": " + self._courses.get(i))
            i += 1

    def printBlockOuts(self):
        if self._blockOuts.size() == 0:
            Console.WriteLine("No blockOuts available")
            return
        Console.WriteLine("BlockOuts:")
        i = 0
        while i < self._blockOuts.size():
            Console.WriteLine("\tBlock " + i + ": " + self._blockOuts.get(i))
            i += 1

    def setSections(self, sections):
        if sections.size() == self._courses.size():
            self._fetchedSections = sections
        else:
            self.setNotification("invalid number of courses retrieved")

    def printSections(self, sections):
        Console.WriteLine("Course chosen:")
        i = 0
        while i < sections.size():
            if i >= self._courses.size():
                break
            Console.WriteLine("\tCourse " + i + " (" + self._courses.get(i) + "): ")
            j = 0
            while j < sections.get(i).size():
                section = sections.get(i).get(j)
                Console.WriteLine("\t\tSection " + j + ": " + section)
                j += 1
            i += 1

    def printSchedules(self, schedules):
        if schedules == None or schedules.size() == 0:
            # System.out.println("wtf");
            return
        Console.WriteLine("Schedules:")
        i = 0
        while i < schedules.size():
            Console.WriteLine("\tSchedule " + i + ":")
            j = 0
            while j < schedules.get(i).size():
                section = schedules.get(i).get(j)
                Console.WriteLine("\t\tCourse " + j + ": " + section)
                j += 1
            i += 1

            # System.out.println("yeah");

    def printFinalSchedules(self, schedules):
        if schedules == None or schedules.size() == 0:
            return
        Console.WriteLine("Schedules: ")
        i = 0
        while i < schedules.size():
            Console.WriteLine("\tSchedule " + i + ":")
            j = 0
            while j < schedules.get(i).size():
                Console.WriteLine("\t\tDay " + j + ": ")
                k = 0
                while k < schedules.get(i).get(j).size():
                    block = schedules.get(i).get(j).get(k)
                    Console.WriteLine("\t\t\t" + block)
                    k += 1
                j += 1
            i += 1

    def filter_sections1(self, fetched_sections):  # one course at a time
        if fetched_sections == None:  # no sections
            return None
        possSections = ArrayList[Section]()
        i = 0
        while i < fetched_sections.size():
            valid = True
            j = 0
            while j < self._blockOuts.size() and valid:
                valid = fetched_sections.get(i).checkNoConflicts(self._blockOuts.get(j))
                j += 1
            if valid:
                possSections.add(fetched_sections.get(i))
            i += 1
        return possSections

    def arrayProduct(self, possSections):
        if possSections == None or possSections.size() == 0:
            # System.out.println("a");
            return None
        else:
            # System.out.println("b");
            i = 0
            while i < possSections.size():
                if possSections.get(i) == None or possSections.get(i).size() == 0:
                    return None
                i += 1
                # System.out.println("c");
        allCombinations = ArrayList[ArrayList]()
        maxNumberOfCombinations = 1
        i = 0
        while i < possSections.size():
            maxNumberOfCombinations *= possSections.get(i).size()
            i += 1
            # System.out.println(maxNumberOfCombinations);
        combinations = Array.CreateInstance(int, maxNumberOfCombinations)
        possSections.size()
        # System.out.println(combinations[0].length);
        # System.out.println(combinations.length);
        courseNum = 0
        while courseNum < combinations[0].length:
            combinations[0][courseNum] = 0
            courseNum += 1
        lastIndexComb = combinations[0].length - 1
        i = 1
        while i < combinations.length:
            j = lastIndexComb
            didNotAddYet = True
            combinations[i][lastIndexComb] = 0
            while j >= 0:
                if didNotAddYet:
                    if combinations[i - 1][j] == possSections.get(j).size() - 1:
                        combinations[i][j] = 0
                    else:
                        combinations[i][j] = combinations[i][j] + 1
                        didNotAddYet = False
                    j -= 1
                else:
                    combinations[i][j] = combinations[i - 1][j]
                    j -= 1
            i += 1
        combinationNum = 0
        while combinationNum < combinations.length:
            allCombinations.add(ArrayList[Section]())
            courseNum = 0
            while courseNum < possSections.size():
                allCombinations.get(combinationNum).add(
                    possSections.get(courseNum).get(combinations[combinationNum][courseNum]))
                courseNum += 1
            combinationNum += 1
        Console.WriteLine("Array Product")
        self.printSchedules(allCombinations)
        return allCombinations

    def filter_sections2(self, possSections):
        if possSections == None or possSections.size() == 0:
            # System.out.println("what");
            return None
        i = 0
        while i < possSections.size():
            if possSections.get(i) == None or possSections.get(i).size() == 0:
                # System.out.println("shit");
                return None
            i += 1
        possibleSchedules = ArrayList[ArrayList]()
        allCombinations = self.arrayProduct(possSections)
        # if(allCombinations == null || allCombinations.size() == 0)
        # return null;
        #
        # for(int i=0;i<allCombinations.size();i++)
        # {
        # if(allCombinations.get(i) == null || allCombinations.get(i).size()==0)
        # return null;
        # }
        comb = 0
        while comb < allCombinations.size():
            valid = True
            course1 = 0
            while course1 < allCombinations.get(comb).size() - 1 and valid:
                course2 = course1 + 1
                while course2 < allCombinations.get(comb).size() and valid:
                    # System.out.print(valid+" " );
                    valid = allCombinations.get(comb).get(course1).checkNoConflicts(
                        allCombinations.get(comb).get(course2))
                    course2 += 1
                course1 += 1
                # System.out.print(valid+" " );
                # System.out.println();
            if valid:
                possibleSchedules.add(allCombinations.get(comb))
            comb += 1
        return possibleSchedules

    def insertBlock(self, block, schedule):
        if block == None or schedule == None:
            return
        else:
            if schedule.size() == 0 or block.getStartTime().lessThan(schedule.get(0).getStartTime()):
                schedule.add(0, block)
            left = 0
            right = schedule.size() - 1
            while left <= right:
                mid = (left + right) / 2
                if schedule.get(mid).getStartTime().lessThan(block.getStartTime()):
                    if mid == schedule.size() - 1 or block.getStartTime().lessThan(
                            schedule.get(mid + 1).getStartTime()):
                        schedule.add(mid + 1, block)
                        return
                    left = mid + 1
                else:
                    if mid - 1 >= 0 and schedule.get(mid - 1).getStartTime().lessThan(block.getStartTime()):
                        schedule.add(mid, block)
                        return
                    right = mid - 1

    def resembleSchedules(self, possibleSchedules):
        schedules = ArrayList[ArrayList]()
        if possibleSchedules == None:
            return None
        if possibleSchedules.size() == 0:
            blockOutSchedule = ArrayList[ArrayList]()
            day = 0
            while day < 7:
                blockOutSchedule.add(ArrayList[Block]())
                day += 1
            blockNum = 0
            while blockNum < self._blockOuts.size():
                blockOut = self._blockOuts.get(blockNum)
                day = 0
                while day < 7:
                    if blockOut.getDays().isOnThatDay(day):
                        self.insertBlock(blockOut, blockOutSchedule.get(day))
                    day += 1
                blockNum += 1
            self._schedules.add(blockOutSchedule)
            return self._schedules
        Console.WriteLine("yes")
        i = 0
        while i < possibleSchedules.size():
            self._schedules.add(ArrayList[ArrayList]())
            day = 0
            while day < 7:
                self._schedules.get(i).add(ArrayList[Block]())
                day += 1
            j = 0
            while j < possibleSchedules.get(i).size():
                k = 0
                while k < 7:
                    if possibleSchedules.get(i).get(j).getDays().isOnThatDay(k):
                        self.insertBlock(possibleSchedules.get(i).get(j), self._schedules.get(i).get(k))
                    k += 1
                j += 1
            i += 1
        Console.WriteLine("yess")
        i = 0
        while i < self._blockOuts.size():
            Console.WriteLine(i)
            j = 0
            while j < self._schedules.size():
                Console.WriteLine("\t" + j)
                k = 0
                while k < 7:
                    Console.WriteLine("\t\t" + k)
                    if self._blockOuts.get(i).getDays().isOnThatDay(k):
                        Console.Write("\t\t\tgot ")
                        self.insertBlock(self._blockOuts.get(i), self._schedules.get(j).get(k))
                        Console.WriteLine("it")
                    k += 1
                j += 1
            i += 1
        return self._schedules

    def calcCommute(self, location1, location2):
        if (location1.compareTo("home") == 0 and location2.compareTo("school") == 0) or (
                        location1.compareTo("school") == 0 or location2.compareTo("home") == 0):
            return self._homeToSchool
        elif (location1.compareTo("home") == 0 and location2.compareTo("work") == 0) or (
                        location1.compareTo("work") == 0 or location2.compareTo("home") == 0):
            return self._workToHome
        elif (location1.compareTo("work") == 0 and location2.compareTo("school") == 0) or (
                        location1.compareTo("school") == 0 or location2.compareTo("work") == 0):
            return self._workToSchool
        else:
            return -1

    def makeCommuteTime(self, location1, location2, dayNum, start):
        travel = self.calcCommute(location1, location2)
        startTime = Time(start.getHours(), start.getMinutes())
        endTime = self.addMinutes(startTime, travel)
        if endTime == None:
            return None
        days = DaysAvailable(False, False, False, False, False, False, False)
        days.setDay(True, dayNum)
        endLocation = System.String(location2)
        return Block("commute", endLocation, startTime, endTime, days)

    def addMinutes(self, time, addMin):
        min = addMin % 60
        hr = addMin / 60 + time.getHours()
        min = min + time.getMinutes()
        hr = hr + min / 60
        min = min % 60
        if hr >= 0 and hr < 24:
            return Time(hr, min)
        if hr == 24 and min == 0:
            return Time(0, 0)
        return None

    def makeStudyTime(self, time, minutesAvailable, day, location):
        if time == None or minutesAvailable <= 0 or (self.getStudyHours() == 0 and self.getStudyMinutes() == 0):
            return None
        dayOn = DaysAvailable(False, False, False, False, False, False, False)
        dayOn.setDay(True, day)
        newTime = Time(time.getHours(), time.getMinutes())
        totalStudy = self.getStudyHours() * 60 + self.getStudyMinutes()
        if totalStudy > minutesAvailable:
            totalStudy = totalStudy - minutesAvailable
            self.setStudyHours(totalStudy / 60)
            self.setStudyMinutes(totalStudy % 60)
            return Block("study", location, newTime, self.addMinutes(time, minutesAvailable), dayOn)
        self.setStudyHours(0)
        self.setStudyMinutes(0)
        return Block("study", location, newTime, self.addMinutes(time, totalStudy), dayOn)

    def insertCommuteTimes(self, schedules):
        if schedules == None:
            return None
        i = 0
        while i < schedules.size():
            valid = True
            j = 0
            while j < schedules.get(i).size() and valid:
                k = 0
                while k < schedules.get(i).get(j).size() and valid:
                    # if(k==0)
                    # {
                    #    block = schedules.get(i).get(j).get(0);
                    # }
                    block = schedules.get(i).get(j).get(k)
                    if k == schedules.get(i).get(j).size() - 1:
                        # if(block.getLocation().compareTo("mobile")==0)
                        # block.setLocation("home");
                        if block.getLocation().compareTo("home") != 0:
                            commute = self.makeCommuteTime(block.getLocation(), "home", j, block.getEndTime())
                            if commute == None:
                                valid = False
                            else:
                                schedules.get(i).get(j).add(k + 1, commute)
                    else:
                        nextBlock = schedules.get(i).get(j).get(k + 1)
                        # if(nextBlock.getLocation().compareTo("mobile")==0)
                        # nextBlock.setLocation(block.getLocation());
                        if nextBlock.getType().compareTo("commute") != 0:
                            if block.getLocation().compareTo(nextBlock.getLocation()) != 0:
                                commute = self.makeCommuteTime(block.getLocation(), nextBlock.getLocation(), j,
                                                               block.getEndTime())
                                if commute == None:
                                    valid = False
                                else:
                                    valid = nextBlock.checkNoConflicts(commute)
                                    schedules.get(i).get(j).add(k + 1, commute)
                    k += 1
                j += 1
            if not valid:
                schedules.remove(i)
                i -= 1
            i += 1
        return schedules

    # public ArrayList<ArrayList<ArrayList<Block>>> insertCommuteTimes(ArrayList<ArrayList<ArrayList<Block>>> schedules)
    # {
    # Block block;
    # boolean valid;
    # String location;
    # if(schedules==null)
    # return null;
    # for(int i=0;i<schedules.size();i++)
    # {
    # valid=true;
    # for(int j=0;j<schedules.get(i).size() && valid;j++)
    # {
    # location="home";
    # if(schedules.get(i).get(j).size()>0)
    # {
    # block = schedules.get(i).get(j).get(0);
    # if(block.getLocation().compareTo("home")!=0 ||
    # block.getLocation().compareTo("mobile")!=0)
    # {
    #
    # }
    # }
    #
    #
    # for(int k=0;k<schedules.get(i).get(j).size() && valid;k++)
    # {
    # block = schedules.get(i).get(j).get(k);
    # Block commute;
    #
    # if(k==schedules.get(i).get(j).size()-1)
    # {
    # if(location.compareTo("home")!=0)
    # {
    # commute = makeCommuteTime(block.getLocation(),"home",j, block.getEndTime());
    # if(commute == null)
    # valid = false;
    # else
    # schedules.get(i).get(j).add(k+1,commute);
    # }
    # }
    # else
    # {
    # Block nextBlock = schedules.get(i).get(j).get(k+1);
    # if(nextBlock.getLocation().compareTo("mobile")==0)
    # continue;
    # if(nextBlock.getType().compareTo("commute")!=0)
    # {
    # if(block.getLocation().compareTo(nextBlock.getLocation())!=0)
    # {
    # commute=makeCommuteTime(block.getLocation(),nextBlock.getLocation(),j,block.getEndTime());
    # if(commute == null)
    # valid=false;
    # else
    # {
    # valid=nextBlock.checkNoConflicts(commute);
    # schedules.get(i).get(j).add(k+1,commute);
    # }
    # }
    # }
    # }
    # }
    # }
    # if(!valid)
    # {
    # schedules.remove(i);
    # i--;
    # }
    # }
    # return schedules;
    # }
    def insertStudyTimes(self, schedules):
        originalMin = self.getStudyMinutes()
        originalHrs = self.getStudyHours()
        if schedules == None:
            return None
        i = 0
        while i < schedules.size():
            j = 0
            while j < schedules.get(i).size():
                k = 0
                while k < schedules.get(i).get(j).size():
                    block = schedules.get(i).get(j).get(k)
                    if k == 0:
                        originalSize = schedules.get(i).get(j).size()
                        time = Time(0, 0)
                        if not (block.getStartTime().equal(time)):
                            studyBlock = self.makeStudyTime(time, time.minutesTo(block.getStartTime()), j, "home")
                            if studyBlock != None:
                                schedules.get(i).get(j).add(0, studyBlock)
                        if originalSize == 1:
                            time = block.getEndTime()
                            nextTime = Time(0, 0)
                            studyBlock = self.makeStudyTime(time, time.minutesTo(nextTime), j, "home")
                            if studyBlock != None:
                                schedules.get(i).get(j).add(studyBlock)
                    elif k == schedules.get(i).get(j).size() - 1:
                        if not (block.getEndTime().equal(Time(0, 0))):
                            time = block.getEndTime()
                            nextTime = Time(0, 0)
                            studyBlock = self.makeStudyTime(time, time.minutesTo(nextTime), j, "home")
                            if studyBlock != None:
                                schedules.get(i).get(j).add(studyBlock)
                    else:
                        nextBlock = schedules.get(i).get(j).get(k + 1)
                        if not (block.getEndTime().equal(nextBlock.getStartTime())):
                            time = block.getEndTime()
                            nextTime = nextBlock.getStartTime()
                            studyBlock = self.makeStudyTime(time, time.minutesTo(nextTime), j, block.getLocation())
                            if studyBlock != None:
                                schedules.get(i).get(j).add(k + 1, studyBlock)
                    k += 1
                j += 1
            if self.getStudyHours() != 0 or self.getStudyMinutes() != 0:
                schedules.remove(i)
                i -= 1
            self.setStudyHours(originalHrs)
            self.setStudyMinutes(originalMin)
            i += 1
        return schedules

    def generateSchedules(self):
        sleep = self.makeSleepBlock()
        if not sleep:
            return False
        Console.WriteLine("\nAfter adding sleep blockOut")
        self.printBlockOuts()
        possibleSchedules = ArrayList[ArrayList](self._courses.size())
        if self._courses.size() > 0:
            if self._fetchedSections.size() == self._courses.size():
                possibleSections = ArrayList[ArrayList]()
                i = 0
                while i < self._fetchedSections.size():
                    possibleSections.add(self.filter_sections1(self._fetchedSections.get(i)))
                    if possibleSections.get(i) == None:
                        self.setNotification("No sections were fetched for a course.")
                        return False
                    if possibleSections.get(i).size() == 0:
                        self.setNotification("All sections for a class conflicted with blockOuts.")
                        return False
                    i += 1
                Console.WriteLine("\nAfter filter1")
                self.printSections(possibleSections)
                possibleSchedules = self.filter_sections2(possibleSections)
                Console.WriteLine("\nAfter filter2")
                self.printSchedules(possibleSchedules)
                if possibleSchedules == None or possibleSchedules.size() == 0:
                    self.setNotification("No possible schedule with this combination of courses and blockOuts.")
                    return False
            else:
                self.setNotification("Incorrect number of courses were fetched")
                return False
        schedules = self.resembleSchedules(possibleSchedules)
        Console.WriteLine("\nAfter converting to schedule format")
        self.printFinalSchedules(self._schedules)
        self._schedules = self.insertCommuteTimes(self._schedules)
        if self._schedules.size() == 0 or self._schedules == None:
            self.setNotification("\nSchedules could not incorporate commute times.")
            return False
        Console.WriteLine("\nAfter inserting commute times")
        self.printFinalSchedules(self._schedules)
        self._schedules = self.insertStudyTimes(self._schedules)
        if self._schedules.size() == 0 or self._schedules == None:
            self.setNotification("\nSchedules had no room for study times.")
            return False
        Console.WriteLine("\nAfter inserting study times")
        self.printFinalSchedules(self._schedules)
        self._schedules = self._schedules
        self.setNotification("\nSchedules were successfully generated.")
        return True
