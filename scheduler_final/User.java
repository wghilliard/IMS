/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import java.util.ArrayList;
/**
 *
 * @author Matthew
 */

public class User {
    private String email;
    private String password;
    private ArrayList<ArrayList<String>> sectionIdSchedules = new ArrayList<ArrayList<String>>();
    private ArrayList<ArrayList<Section>> sectionSchedules = new ArrayList<ArrayList<Section>>();
    private ArrayList<ArrayList<ArrayList<Block>>> schedules = new ArrayList<ArrayList<ArrayList<Block>>>();
    private ArrayList<ArrayList<Section>> fetchedSections = new ArrayList<ArrayList<Section>>();
    private int workToSchool;
    private int homeToSchool;
    private int workToHome;
    private int sleepHours;
    private int sleepMinutes;
    private int studyHours;
    private int studyMinutes;
    private Block sleepBlock;
    private ArrayList<Block> blockOuts = new ArrayList<Block>();
    private ArrayList<String> courses = new ArrayList<String>();
    private String notification;

    public User(int workToHome, int workToSchool, int homeToSchool, int sleepHours, int sleepMinutes,
            int studyHours, int studyMinutes)
    {
        email="dogTeam";
        password="yeah";
        setWorkToSchool(workToSchool);
        setHomeToSchool(homeToSchool);
        setWorkToHome(workToHome);
        setSleepHours(sleepHours);
        setSleepMinutes(sleepMinutes);
        setStudyHours(studyHours);
        setStudyMinutes(studyMinutes);
    }

    public int getStudyHours() {
        return studyHours;
    }

    public void setStudyHours(int studyHours) {
        if(studyHours>=0)
            this.studyHours = studyHours;
        else
            this.studyHours = 0;
    }

    public int getStudyMinutes() {
        return studyMinutes;
    }

    public void setStudyMinutes(int studyMinutes) {
        if(studyMinutes>=0)
            this.studyMinutes = studyMinutes;
        else
            this.studyMinutes = 0;
    }

    public void setWorkToSchool(int workToSchool) {
        if(workToSchool>=0 && workToSchool<24*60)
            this.workToSchool = workToSchool;
        else
            this.workToSchool = 0;
    }

    public void setHomeToSchool(int homeToSchool) {
        if(homeToSchool>=0 && homeToSchool<24*60)
            this.homeToSchool = homeToSchool;
        else
            this.homeToSchool = 0;
    }

    public void setWorkToHome(int workToHome) {
        if(workToHome>=0 && workToHome<24*60)
            this.workToHome = workToHome;
        else
            this.workToHome = 0;
    }

    public void setNotification(String notification) {
        this.notification = notification;
    }

    public int getSleepHours() {
        return sleepHours;
    }

    public void setSleepHours(int sleepHours) {
        if(sleepHours>=6 && sleepHours<=24)
            this.sleepHours = sleepHours;
        else
            this.sleepHours = 6;
    }

    public int getSleepMinutes() {
        return sleepMinutes;
    }

    public void setSleepMinutes(int sleepMinutes) {
        if(sleepHours == 24)
            this.sleepMinutes = 0;
        else if(sleepMinutes >=0 && sleepMinutes <60)
            this.sleepMinutes = sleepMinutes;
        else
            this.sleepMinutes = 0;
    }

    public boolean makeSleepBlock()
    {
        DaysAvailable daysAvailable = new DaysAvailable(true,true,true,true,true,true,true);
        this.sleepBlock = new Block("sleep","home",new Time(0,0),new Time(getSleepHours(),getSleepMinutes()),daysAvailable);
        boolean valid = addBlockOut(sleepBlock);
        if(!valid)
        {
            setNotification("No room for mandatory sleep!");
            return false;
        }
        return true;
    }

    public int getWorkToSchool() {
        return workToSchool;
    }

    public int getHomeToSchool() {
        return homeToSchool;
    }

    public int getWorkToHome() {
        return workToHome;
    }

    public String getNotification() {
        return notification;
    }

    public boolean addCourse(String course)
    {
        for(int i =0; i<courses.size();i++)
        {
            if(courses.get(i).compareTo(course)==0)
            {
                setNotification("Course was not added becuase it matched one"
                        + " of your existing courses.");
                return false;
            }
        }
        courses.add(course);
        setNotification("Course is successfully added.");
        return true;
    }

    public ArrayList<String> getCourses()
    {
        return this.courses;
    }

    public boolean addBlockOut(Block blockOut)
    {
        setNotification("");
        boolean valid=true;
        for(int i=0;i<blockOuts.size();i++)
        {
            if(!(blockOut.checkNoConflicts(blockOuts.get(i))))
            {
                setNotification("BlockOut conflicted with other blockOuts");
                valid=false;
            }
        }
        if(!valid)
            return false;
        blockOuts.add(blockOut);
        setNotification("BlockOut was successfully added");
        return true;
    }

    public void printCourses()
    {
        if(courses.size()==0)
        {
            System.out.println("No courses available");
            return;
        }
        System.out.println("Courses:");
        for(int i =0; i<courses.size(); i++)
        {
            System.out.println("\tCourse "+i+": "+courses.get(i));
        }
    }

    public void printBlockOuts()
    {
        if(blockOuts.size()==0)
        {
            System.out.println("No blockOuts available");
            return;
        }
        System.out.println("BlockOuts:");
        for(int i = 0; i<blockOuts.size();i++)
        {
            System.out.println("\tBlock " +i +": "+blockOuts.get(i));
        }
    }

    public boolean setSections(ArrayList<ArrayList<Section>> sections)
    {
        if(sections.size() == courses.size())
        {
            this.fetchedSections = sections;
            return true;
        }
        else
        {
            setNotification("invalid number of courses retrieved");
            return false;
        }
    }

    public ArrayList<ArrayList<Section>> getSections()
    {
        return fetchedSections;
    }

    public void printSections(ArrayList<ArrayList<Section>> sections)
    {
        Section section;
        System.out.println("Course chosen:");
        for(int i=0;i<sections.size();i++)
        {
            if(i>=courses.size())
                break;
            System.out.println("\tCourse "+i+" ("+courses.get(i)+"): ");
            for(int j=0;j<sections.get(i).size();j++)
            {
                section = sections.get(i).get(j);
                System.out.println("\t\tSection " + j + ": " +section);
            }
        }
    }

    public void printSchedules(ArrayList<ArrayList<Section>> schedules)
    {
        if(schedules == null || schedules.size()==0)
        {
            //System.out.println("wtf");
            return;
        }
        Section section;
        System.out.println("Schedules:");
        for(int i=0;i<schedules.size();i++)
        {
            System.out.println("\tSchedule "+i+":");
            for(int j=0;j<schedules.get(i).size();j++)
            {
                section = schedules.get(i).get(j);
                System.out.println("\t\tCourse " +j+": "+section);
            }
        }
        //System.out.println("yeah");
    }

    public void printFinalSchedules(ArrayList<ArrayList<ArrayList<Block>>> schedules)
    {
        if(schedules == null || schedules.size()==0)
            return;
        Block block;
        System.out.println("Schedules: ");
        for(int i=0;i<schedules.size();i++)
        {
            System.out.println("\tSchedule "+i+":");
            for(int j=0;j<schedules.get(i).size();j++)
            {
                System.out.println("\t\tDay " +j+": ");
                for(int k=0;k<schedules.get(i).get(j).size();k++)
                {
                    block = schedules.get(i).get(j).get(k);
                    System.out.println("\t\t\t"+block);
                }
            }
        }
    }

    public ArrayList<ArrayList<ArrayList<Block>>> getFinalSchedules()
    {
        return schedules;
    }

    public ArrayList<ArrayList<Section>> getSectionSchedules()
    {
        return sectionSchedules;
    }

    public boolean setSectionIDs()
    {
        boolean valid = true;
        int i, j;
        for(i=0;i<sectionSchedules.size();i++)
        {
            if(sectionSchedules.get(i)==null || sectionSchedules.get(i).size() != courses.size())
                valid = false;
        }
        if((!valid) || sectionSchedules.size()==0)
            return false;
        for(i=0;i<sectionSchedules.size();i++)
        {
            sectionIdSchedules.add(new ArrayList<String>());
            for(j=0;j<sectionSchedules.get(i).size();j++)
                sectionIdSchedules.get(i).add(sectionSchedules.get(i).get(j).getID());
        }
        return true;
    }

    public ArrayList<ArrayList<String>> getSectionIDs()
    {
        return sectionIdSchedules;
    }

    public void printSectionIDs()
    {
        if(sectionIdSchedules == null || sectionIdSchedules.size() == 0)
            return;
        System.out.println("Section IDs by schedule:");
        for(int i=0;i<sectionIdSchedules.size();i++)
        {
            System.out.println("\tSchedule "+i);
            for(int j=0;j<sectionIdSchedules.get(i).size();j++)
                System.out.println("\t\t"+sectionIdSchedules.get(i).get(j));
        }
    }

    public ArrayList<Section> filter_sections1(ArrayList<Section> fetched_sections) // one course at a time
    {
        if(fetched_sections == null) // no sections
            return null;

        ArrayList<Section> possSections = new ArrayList<Section>();
        boolean valid;
        for(int i=0;i<fetched_sections.size();i++)
        {
            valid=true;
            for(int j=0;j<blockOuts.size()&&valid;j++)
            {
                valid = fetched_sections.get(i).checkNoConflicts(blockOuts.get(j));
            }
            if(valid)
                possSections.add(fetched_sections.get(i));
        }
        return possSections;
    }


    public ArrayList<ArrayList<Section>> arrayProduct(ArrayList<ArrayList<Section>> possSections)
    {
        if(possSections == null || possSections.size()==0)
        {
            //System.out.println("a");
            return null;
        }
        else
        {
            //System.out.println("b");
            for(int i=0;i<possSections.size();i++)
            {
                if(possSections.get(i) == null || possSections.get(i).size()==0)
                    return null;
            }
            //System.out.println("c");
        }
        ArrayList<ArrayList<Section>> allCombinations = new ArrayList<ArrayList<Section>>();
        int maxNumberOfCombinations = 1;
        for(int i=0;i<possSections.size();i++)
        {
            maxNumberOfCombinations*=possSections.get(i).size();
        }
        //System.out.println(maxNumberOfCombinations);
        int[][] combinations = new int[maxNumberOfCombinations][possSections.size()];
        //System.out.println(combinations[0].length);
        //System.out.println(combinations.length);
        for(int courseNum =0;courseNum<combinations[0].length;courseNum++)
        {
            combinations[0][courseNum]=0;
        }
        int j;
        boolean didNotAddYet;
        int lastIndexComb = combinations[0].length-1;
        for(int i=1;i<combinations.length;i++)
        {
            j = lastIndexComb;
            didNotAddYet = true;
            combinations[i][lastIndexComb] = combinations[i-1][lastIndexComb];
            while(j>=0)
            {
                if(didNotAddYet)
                {
                    if(combinations[i-1][j]==possSections.get(j).size()-1)
                        combinations[i][j] = 0;
                    else
                    {
                        combinations[i][j] = combinations[i-1][j]+1;
                        didNotAddYet=false;
                    }
                    j--;
                }
                else
                {
                    combinations[i][j] = combinations[i-1][j];
                    j--;
                }
            }
        }

        for(int combinationNum=0;combinationNum<combinations.length;combinationNum++)
        {
            allCombinations.add(new ArrayList<Section>());
            for(int courseNum=0; courseNum<possSections.size();courseNum++)
            {
                allCombinations.get(combinationNum).add(possSections.get(courseNum).get(combinations[combinationNum][courseNum]));
            }
        }
        //System.out.println("Array Product");
        //printSchedules(allCombinations);
        return allCombinations;
    }

    public ArrayList<ArrayList<Section>> filter_sections2(ArrayList<ArrayList<Section>> possSections)
    {
        if(possSections == null || possSections.size() == 0)
        {
            //System.out.println("what");
            return null;
        }
        for(int i=0;i<possSections.size();i++)
        {
            if(possSections.get(i) == null || possSections.get(i).size()==0)
            {
                //System.out.println("shit");
                return null;
            }

        }
        ArrayList<ArrayList<Section>> possibleSchedules = new ArrayList<ArrayList<Section>>();
        ArrayList<ArrayList<Section>> allCombinations = arrayProduct(possSections);
        /*if(allCombinations == null || allCombinations.size() == 0)
            return null;

        for(int i=0;i<allCombinations.size();i++)
        {
            if(allCombinations.get(i) == null || allCombinations.get(i).size()==0)
                return null;
        }*/
        boolean valid;
        for(int comb=0;comb<allCombinations.size();comb++)
        {
            valid=true;
            for(int course1=0;course1<allCombinations.get(comb).size()-1 && valid;course1++)
            {
                for(int course2=course1+1;course2<allCombinations.get(comb).size() && valid;course2++)
                {
                    //System.out.print(valid+" " );
                    valid=allCombinations.get(comb).get(course1).checkNoConflicts(allCombinations.get(comb).get(course2));
                    //System.out.print(valid+" " );
                }
            }
            //System.out.println();
            if(valid)
                possibleSchedules.add(allCombinations.get(comb));
        }
        return possibleSchedules;
    }

    public void insertBlock(Block block, ArrayList<Block> schedule)
    {
        if(block==null || schedule ==null)
            return;
        else
        {
            if(schedule.size()==0 || block.getStartTime().lessThan(schedule.get(0).getStartTime()))
            {
                schedule.add(0,block);
            }
            int mid;
            int left=0;
            int right=schedule.size()-1;
            while(left<=right)
            {
                mid=(left+right)/2;
                if(schedule.get(mid).getStartTime().lessThan(block.getStartTime()))
                {
                    if(mid==schedule.size()-1 || block.getStartTime().lessThan(
                    schedule.get(mid+1).getStartTime()))
                    {
                        schedule.add(mid+1,block);
                        return;
                    }
                    left=mid+1;
                }
                else
                {
                    if(mid-1>=0 && schedule.get(mid-1).getStartTime().lessThan(block.getStartTime()))
                    {
                        schedule.add(mid,block);
                        return;
                    }
                    right=mid-1;
                }
            }
        }
    }

    public ArrayList<ArrayList<ArrayList<Block>>> resembleSchedules(ArrayList<ArrayList<Section>> possibleSchedules)
    {
        ArrayList<ArrayList<ArrayList<Block>>> schedules = new ArrayList<ArrayList<ArrayList<Block>>>();
        if(possibleSchedules==null)
            return null;
        if(possibleSchedules.size()==0)
        {
            ArrayList<ArrayList<Block>> blockOutSchedule = new ArrayList<ArrayList<Block>>();
            Block blockOut;
            for(int day = 0;day<7;day++)
                blockOutSchedule.add(new ArrayList<Block>());
            for(int blockNum=0;blockNum<blockOuts.size();blockNum++)
            {
                blockOut = blockOuts.get(blockNum);
                for(int day = 0;day<7;day++)
                {
                    if(blockOut.getDays().isOnThatDay(day))
                    {
                        insertBlock(blockOut,blockOutSchedule.get(day));
                    }
                }
            }
            schedules.add(blockOutSchedule);
            return schedules;
        }
        //System.out.println("yes");
        for(int i=0;i<possibleSchedules.size();i++)
        {
            schedules.add(new ArrayList<ArrayList<Block>>());
            for(int day = 0;day<7;day++)
                schedules.get(i).add(new ArrayList<Block>());
            for(int j=0;j<possibleSchedules.get(i).size();j++)
            {
                for(int k=0;k<7;k++)
                {
                    if(possibleSchedules.get(i).get(j).getDays().isOnThatDay(k))
                    {
                        insertBlock(possibleSchedules.get(i).get(j),schedules.get(i).get(k));
                    }
                }
            }
        }
        //System.out.println("yess");
        for(int i=0;i<blockOuts.size();i++)
        {
            //System.out.println(i);
            for(int j=0;j<schedules.size();j++)
            {
                //System.out.println("\t"+j);
                for(int k=0;k<7;k++)
                {
                    //System.out.println("\t\t"+k);
                    if(blockOuts.get(i).getDays().isOnThatDay(k))
                    {
                        //System.out.print("\t\t\tgot ");
                        insertBlock(blockOuts.get(i),schedules.get(j).get(k));

                       //System.out.println("it");
                    }
                }
            }
        }
        return schedules;
    }

    public int calcCommute(String location1, String location2)
    {
        if((location1.compareTo("home")==0 && location2.compareTo("school")==0) ||
                (location1.compareTo("school")==0 || location2.compareTo("home")==0))
            return homeToSchool;
        else if((location1.compareTo("home")==0 && location2.compareTo("work")==0) ||
                (location1.compareTo("work")==0 || location2.compareTo("home")==0))
            return workToHome;
        else if((location1.compareTo("work")==0 && location2.compareTo("school")==0) ||
                (location1.compareTo("school")==0 || location2.compareTo("work")==0))
            return workToSchool;
        else
            return -1;
    }

    public Block makeCommuteTime(String location1, String location2, int dayNum, Time start)
    {
        int travel = calcCommute(location1,location2);
        Time startTime = new Time(start.getHours(),start.getMinutes());
        Time endTime = addMinutes(startTime, travel);
        if(endTime == null)
            return null;
        DaysAvailable days = new DaysAvailable(false,false,false,false,false,false,false);
        days.setDay(true,dayNum);
        String endLocation = new String(location2);
        return new Block("commute",endLocation,startTime,endTime, days);
    }

    public Time addMinutes(Time time, int addMin)
    {
        if(addMin==0 || time == null)
            return null;
        int min = addMin%60;
        int hr = addMin/60 + time.getHours();
        min = min + time.getMinutes();
        hr = hr + min/60;
        min = min%60;
        if(hr>=0 && hr<24)
        {
            return new Time(hr, min);
        }
        if(hr == 24 && min==0)
        {
            return new Time(0,0);
        }
        return null;
    }

    public Block makeStudyTime(Time time, int minutesAvailable, int day, String location)
    {
        if(time == null || minutesAvailable<=0 || (getStudyHours() == 0 && getStudyMinutes() ==0))
            return null;

        DaysAvailable dayOn = new DaysAvailable(false,false,false,false,false,false,false);
        dayOn.setDay(true,day);
        Time newTime = new Time(time.getHours(), time.getMinutes());

        int totalStudy = getStudyHours()*60 + getStudyMinutes();
        if(totalStudy>minutesAvailable)
        {
            totalStudy = totalStudy - minutesAvailable;
            setStudyHours(totalStudy/60);
            setStudyMinutes(totalStudy%60);
            return new Block("study",location,newTime,addMinutes(time,minutesAvailable),dayOn);
        }
        setStudyHours(0);
        setStudyMinutes(0);
        return new Block("study",location,newTime,addMinutes(time,totalStudy),dayOn);
    }

    public ArrayList<ArrayList<ArrayList<Block>>> insertCommuteTimes(ArrayList<ArrayList<ArrayList<Block>>> schedules)
    {
        Block block;
        boolean valid;
        if(schedules==null)
            return null;
        for(int i=0;i<schedules.size();i++)
        {
            valid=true;
            for(int j=0;j<schedules.get(i).size() && valid;j++)
            {
                for(int k=0;k<schedules.get(i).get(j).size() && valid;k++)
                {
                    //if(k==0)
                    //{
                    //    block = schedules.get(i).get(j).get(0);
                    //}
                    block = schedules.get(i).get(j).get(k);
                    Block commute;

                    if(k==schedules.get(i).get(j).size()-1)
                    {
                        //if(block.getLocation().compareTo("mobile")==0)
                            //block.setLocation("home");
                        if(block.getLocation().compareTo("home")!=0)
                        {
                            if(calcCommute(block.getLocation(),"home")<=block.getEndTime().minutesTo(new Time(0,0)))
                            {
                                commute = makeCommuteTime(block.getLocation(),"home",j, block.getEndTime());
                                if(commute!=null)
                                    schedules.get(i).get(j).add(k+1,commute);
                            }
                            else
                                valid=false;
                        }
                    }
                    else
                    {
                        Block nextBlock = schedules.get(i).get(j).get(k+1);
                        //if(nextBlock.getLocation().compareTo("mobile")==0)
                            //nextBlock.setLocation(block.getLocation());
                        if(nextBlock.getType().compareTo("commute")!=0)
                        {
                            if(block.getLocation().compareTo(nextBlock.getLocation())!=0)
                            {
                                if(calcCommute(block.getLocation(),nextBlock.getLocation())<=block.getEndTime().minutesTo(new Time(0,0)))
                                {
                                    commute=makeCommuteTime(block.getLocation(),nextBlock.getLocation(),j,block.getEndTime());
                                    if(commute != null)
                                    {
                                        valid=nextBlock.checkNoConflicts(commute);
                                        schedules.get(i).get(j).add(k+1,commute);
                                    }
                                }
                                else
                                    valid=false;
                            }
                        }
                    }
                }
            }
            if(!valid)
            {
                if(sectionSchedules != null && sectionSchedules.size()!=0)
                    sectionSchedules.remove(i);
                schedules.remove(i);
                i--;
            }
        }
        return schedules;
    }

    /*public ArrayList<ArrayList<ArrayList<Block>>> insertCommuteTimes(ArrayList<ArrayList<ArrayList<Block>>> schedules)
    {
        Block block;
        boolean valid;
        String location;
        if(schedules==null)
            return null;
        for(int i=0;i<schedules.size();i++)
        {
            valid=true;
            for(int j=0;j<schedules.get(i).size() && valid;j++)
            {
                location="home";
                if(schedules.get(i).get(j).size()>0)
                {
                    block = schedules.get(i).get(j).get(0);
                    if(block.getLocation().compareTo("home")!=0 ||
                            block.getLocation().compareTo("mobile")!=0)
                    {

                    }
                }


                for(int k=0;k<schedules.get(i).get(j).size() && valid;k++)
                {
                    block = schedules.get(i).get(j).get(k);
                    Block commute;

                    if(k==schedules.get(i).get(j).size()-1)
                    {
                        if(location.compareTo("home")!=0)
                        {
                            commute = makeCommuteTime(block.getLocation(),"home",j, block.getEndTime());
                            if(commute == null)
                                valid = false;
                            else
                                schedules.get(i).get(j).add(k+1,commute);
                        }
                    }
                    else
                    {
                        Block nextBlock = schedules.get(i).get(j).get(k+1);
                        if(nextBlock.getLocation().compareTo("mobile")==0)
                            continue;
                        if(nextBlock.getType().compareTo("commute")!=0)
                        {
                            if(block.getLocation().compareTo(nextBlock.getLocation())!=0)
                            {
                                commute=makeCommuteTime(block.getLocation(),nextBlock.getLocation(),j,block.getEndTime());
                                if(commute == null)
                                    valid=false;
                                else
                                {
                                    valid=nextBlock.checkNoConflicts(commute);
                                    schedules.get(i).get(j).add(k+1,commute);
                                }
                            }
                        }
                    }
                }
            }
            if(!valid)
            {
                schedules.remove(i);
                i--;
            }
        }
        return schedules;
    }*/

    public ArrayList<ArrayList<ArrayList<Block>>> insertStudyTimes(ArrayList<ArrayList<ArrayList<Block>>> schedules)
    {
        Block block;
        Block studyBlock;
        Time time;
        Time nextTime;
        int originalMin = getStudyMinutes();
        int originalHrs = getStudyHours();;
        if(schedules==null)
            return null;
        for(int i=0;i<schedules.size();i++)
        {
            for(int j=0;j<schedules.get(i).size();j++)
            {
                for(int k=0;k<schedules.get(i).get(j).size();k++)
                {
                    block = schedules.get(i).get(j).get(k);
                    if(k==0)
                    {
                        int originalSize=schedules.get(i).get(j).size();
                        time = new Time(0,0);
                        if(!(block.getStartTime().equal(time)))
                        {
                            studyBlock=makeStudyTime(time,time.minutesTo(block.getStartTime()),j,"home");
                            if(studyBlock!=null)
                            {
                                schedules.get(i).get(j).add(0,studyBlock);
                            }
                        }
                        if(originalSize==1)
                        {
                            time = block.getEndTime();
                            nextTime = new Time(0,0);
                            studyBlock=makeStudyTime(time,time.minutesTo(nextTime),j,"home");
                            if(studyBlock!=null)
                            {
                                schedules.get(i).get(j).add(studyBlock);
                            }
                        }

                    }
                    else if(k==schedules.get(i).get(j).size()-1)
                    {
                        if(!(block.getEndTime().equal(new Time(0,0))))
                        {
                            time = block.getEndTime();
                            nextTime = new Time(0,0);
                            studyBlock=makeStudyTime(time,time.minutesTo(nextTime),j,"home");
                            if(studyBlock!=null)
                            {
                                schedules.get(i).get(j).add(studyBlock);
                            }
                        }
                    }
                    else
                    {
                        Block nextBlock = schedules.get(i).get(j).get(k+1);
                        if(!(block.getEndTime().equal(nextBlock.getStartTime())))
                        {
                            time = block.getEndTime();
                            nextTime = nextBlock.getStartTime();
                            studyBlock=makeStudyTime(time,time.minutesTo(nextTime),j,block.getLocation());
                            if(studyBlock!=null)
                            {
                                schedules.get(i).get(j).add(k+1,studyBlock);
                            }
                        }
                    }
                }
            }
            if(getStudyHours()!=0 || getStudyMinutes()!=0)
            {
                if(sectionSchedules != null && sectionSchedules.size()!=0)
                    sectionSchedules.remove(i);
                schedules.remove(i);
                i--;
            }
            setStudyHours(originalHrs);
            setStudyMinutes(originalMin);
        }
        return schedules;
    }

    public boolean generateSchedules()
    {
        boolean sleep = makeSleepBlock();
        if(!sleep)
            return false;
        //System.out.println("\nAfter adding sleep blockOut");
        //printBlockOuts();
        ArrayList<ArrayList<Section>> possibleSchedules= new ArrayList<ArrayList<Section>>(courses.size());
        if(courses.size()>0)
        {
            if(fetchedSections.size() == courses.size())
            {
                ArrayList<ArrayList<Section>> possibleSections = new ArrayList<ArrayList<Section>>();

                for(int i = 0; i<fetchedSections.size();i++)
                {
                    possibleSections.add(filter_sections1(fetchedSections.get(i)));
                    if(possibleSections.get(i)==null)
                    {
                        setNotification("No sections were fetched for a course.");
                        return false;
                    }
                    if(possibleSections.get(i).size()==0)
                    {
                        setNotification("All sections for a class conflicted with blockOuts.");
                        return false;
                    }
                }
                //System.out.println("\nAfter filter1");
                //printSections(possibleSections);
                possibleSchedules = filter_sections2(possibleSections);
                //System.out.println("\nAfter filter2");
                //printSchedules(possibleSchedules);
                if(possibleSchedules == null || possibleSchedules.size() == 0)
                {
                    setNotification("No possible schedule with this combination of courses and blockOuts.");
                    return false;
                }
            }
            else
            {
                setNotification("Incorrect number of courses were fetched");
                return false;
            }
        }

        this.sectionSchedules = possibleSchedules;
        ArrayList<ArrayList<ArrayList<Block>>> schedules = resembleSchedules(possibleSchedules);
        //System.out.println("\nAfter converting to schedule format");
        //printFinalSchedules(schedules);
        schedules=insertCommuteTimes(schedules);
        if(schedules.size()==0 || schedules == null)
        {
            setNotification("\nSchedules could not incorporate commute times.");
            return false;
        }
        //System.out.println("\nAfter inserting commute times");
        //printFinalSchedules(schedules);

        schedules=insertStudyTimes(schedules);
        if(schedules.size()==0 || schedules == null)
        {
            setNotification("\nSchedules had no room for study times.");
            return false;
        }
        //System.out.println("\nAfter inserting study times");
        //printFinalSchedules(schedules);
        this.schedules = schedules;
        this.setSectionIDs();
        //this.printSectionIDs();
        setNotification("\nSchedules were successfully generated.");
        return true;
    }
}