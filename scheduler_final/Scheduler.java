/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
import java.util.ArrayList;
//import javax.json.*;


 
import java.io.FileReader;
import java.io.FileWriter;
//import java.util.Iterator;
 
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
/*import com.mongodb.MongoClientURI;
import com.mongodb.MongoClient;
import com.mongodb.client.MongoDatabase;*/
/**
 *
 * @author Matthew
 */
public class Scheduler {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        // TODO code application logic here
        /*MongoClientURI connectionString = new MongoClientURI("mongodb://localhost:27017");
        MongoClient mongoClient = new MongoClient(connectionString);

        MongoDatabase database = mongoClient.getDatabase("quartermaster");*/
        User dog = new User(0,0,0,0,0,0,0);
        
        dog = inputFile(dog,args[0]);
        
        JSONObject obj = outputFile(dog,args[0]);
        
        if(obj==null)
            System.out.println("File was not written!");
        else
            System.out.println(obj);
        
        //Test Case 1
        /*User dog1 = new User(10,10,10,6,0,30,43);
        dog1.addCourse("CSE 1315");
        System.out.println(dog1.getNotification());
        dog1.addCourse("MATH 3330");
        System.out.println(dog1.getNotification());
        dog1.addCourse("MATH 3350");
        System.out.println(dog1.getNotification());
        ArrayList<ArrayList<Section>> courseSectionData = new ArrayList<ArrayList<Section>>();
        courseSectionData.add(new ArrayList<Section>());
        int[] repeat = {0,1,0,1,0,1,0};
        courseSectionData.get(0).add(new Section("CSE 1315-001",new Time(10,0),new Time(10,50),
            new DaysAvailable(false,true,false,true,false,true,false),"","","A"));
        int[] repeat2 = {0,0,1,0,1,0,0};
        courseSectionData.get(0).add(new Section("CSE 1315-002",new Time(16,0),new Time(17,20),
            new DaysAvailable(false,false,true,false,true,false,false),"","","B"));
        courseSectionData.add(new ArrayList<Section>());
        courseSectionData.get(1).add(new Section("MATH 3330-001",new Time(11,0),new Time(12,00),
            new DaysAvailable(false,true,false,true,false,true,false),"","","C"));
        courseSectionData.get(1).add(new Section("MATH 3330-002",new Time(20,10),new Time(21,20),
            new DaysAvailable(false,false,true,false,true,false,false),"","","D"));
        int[] repeat3 = {0,0,1,0,0,0,0};
        courseSectionData.get(1).add(new Section("MATH 3330-003",new Time(22,0),new Time(23,50),
            new DaysAvailable(false,false,true,false,false,false,false),"","","E"));
        courseSectionData.add(new ArrayList<Section>());
        courseSectionData.get(2).add(new Section("MATH 3350-001",new Time(13,0),new Time(14,00),
            new DaysAvailable(false,true,false,true,false,true,false),"","","F"));
        courseSectionData.get(2).add(new Section("MATH 3350-002",new Time(12,59),new Time(14,20),
            new DaysAvailable(false,false,true,false,true,false,false),"","","G"));
        courseSectionData.get(2).add(new Section("MATH 3350-003",new Time(12,30),new Time(15,20),
            new DaysAvailable(false,false,true,false,false,false,false),"","","H"));
        //dog1.addCourse("yes");
        //System.out.println(dog1.getNotification());
        //int[] repetition = {1,1,1,1,1,1,1};
        //dog1.addBlockOut(new Block("sleep","home",new Time(0,0),new Time(6,0),repetition));
        //System.out.println(dog1.getNotification());
        dog1.addBlockOut(new Block("work","work",new Time(12,30),new Time(12,50),
            new DaysAvailable(true,true,true,true,true,true,true)));
        System.out.println(dog1.getNotification());
        dog1.addBlockOut(new Block("work","work",new Time(6,30),new Time(12,0),
            new DaysAvailable(true,true,true,true,true,true,true)));
        System.out.println(dog1.getNotification());
        dog1.addBlockOut(new Block("other","work",new Time (21,30),new Time(23,0),
            new DaysAvailable(true,true,true,true,true,true,true)));
        System.out.println(dog1.getNotification());
        dog1.addBlockOut(new Block("other","work",new Time (19,30),new Time(20,0),
            new DaysAvailable(true,true,true,true,true,true,true)));
        System.out.println(dog1.getNotification());
        dog1.setSections(courseSectionData);
        System.out.println("\nCurrent BlockOuts");
        dog1.printBlockOuts();
        System.out.println("\nCurrent Courses");
        dog1.printCourses();
        System.out.println("\nFetched Sections Information");
        dog1.printSections(courseSectionData);
        dog1.generateSchedules();
        System.out.println(dog1.getNotification());
        
        //User dog2 = new User(20,10,50,10,6);
        //dog2.addCourse("yes");
        //System.out.println(dog2.getNotification());
        //dog2.addCourse("what");
        //System.out.println(dog2.getNotification());
        //dog2.addCourse("yes");
        //System.out.println(dog2.getNotification());*/
    }
    
    public static User inputFile(User dog, String fileName)
    {
        try {
            
            JSONParser parser = new JSONParser();
 
            //Object obj = parser.parse(new FileReader(
                    //"./tmp/in/"+fileName));
            Object obj = parser.parse(new FileReader(
                    "/Users/wghilliard/PycharmProjects/IMS/scheduler_final/tmp/in/"+fileName));
                    
            JSONObject jsonObject = (JSONObject) obj;
 
            int study = Integer.parseInt((String)(jsonObject.get("study")));
            JSONObject commute  = (JSONObject) jsonObject.get("commute");
            int workToHome = Integer.parseInt((String)(commute.get("workToHome")));
            int workToSchool = Integer.parseInt((String)(commute.get("workToSchool")));
            int homeToSchool = Integer.parseInt((String)(commute.get("homeToSchool")));
            int sleep = Integer.parseInt((String)(jsonObject.get("sleep")));
            JSONArray blockOuts = (JSONArray)(jsonObject.get("block_outs"));
            JSONArray courses = (JSONArray)(jsonObject.get("classes"));
            JSONObject sections = (JSONObject) (jsonObject.get("sections"));
            
            dog = new User(workToHome,workToSchool,homeToSchool,sleep,0,study,0);
            
            //System.out.println("study: " + study);
            //System.out.println("sleep: " + sleep);
            
            //System.out.println("Commute Times:");
            //System.out.println("\tworkToHome: "+workToHome);
            //System.out.println("\tworkToSchool: "+workToSchool);
            //System.out.println("\thomeToSchool: "+homeToSchool);
            //System.out.println();
            
            boolean valid = true;
            int startHours;
            int startMinutes;
            int endHours;
            int endMinutes;
            DaysAvailable days;
            String location;
            String type;
            JSONObject blockOut;
            JSONObject startTime;
            JSONObject endTime;
            JSONObject repetition;
            
            for(int i=0;i<blockOuts.size();i++)
            {
                days = new DaysAvailable(false,false,false,false,false,false,false);
                
                blockOut = (JSONObject) blockOuts.get(i);
                
                type = (String) blockOut.get("name");
                location = (String) blockOut.get("location");
                
                startTime = (JSONObject) blockOut.get("start_time");
                startHours = Integer.parseInt((String)(startTime.get("hour")));
                startMinutes = Integer.parseInt((String)(startTime.get("minute")));
                
                endTime = (JSONObject) blockOut.get("end_time");
                endHours = Integer.parseInt((String)(endTime.get("hour")));
                endMinutes = Integer.parseInt((String)(endTime.get("minute")));
                
                repetition = (JSONObject) blockOut.get("repetition");
                
                if(repetition.get("sun") instanceof Boolean)
                    days.setSun((boolean) repetition.get("sun"));
                else if(repetition.get("sun") instanceof String)
                    days.setSun(Boolean.parseBoolean((String) repetition.get("sun")));
                    
                if(repetition.get("mon") instanceof Boolean)
                    days.setMon((boolean) repetition.get("mon"));
                else if(repetition.get("mon") instanceof String)
                    days.setMon(Boolean.parseBoolean((String) repetition.get("mon")));
                    
                if(repetition.get("tues") instanceof Boolean)
                    days.setTues((boolean) repetition.get("tues"));
                else if(repetition.get("tues") instanceof String)
                    days.setTues(Boolean.parseBoolean((String) repetition.get("tues")));
                    
                if(repetition.get("weds") instanceof Boolean)
                    days.setWed((boolean) repetition.get("weds"));
                else if(repetition.get("weds") instanceof String)
                    days.setWed(Boolean.parseBoolean((String) repetition.get("weds")));
                    
                if(repetition.get("thurs") instanceof Boolean)
                    days.setThurs((boolean) repetition.get("thurs"));
                else if(repetition.get("thurs") instanceof String)
                    days.setThurs(Boolean.parseBoolean((String) repetition.get("thurs")));
                    
                if(repetition.get("fri") instanceof Boolean)
                    days.setFri((boolean) repetition.get("fri"));
                else if(repetition.get("fri") instanceof String)
                    days.setFri(Boolean.parseBoolean((String) repetition.get("fri")));
                    
                if(repetition.get("sat") instanceof Boolean)
                    days.setSat((boolean) repetition.get("sat"));
                else if(repetition.get("sat") instanceof String)
                    days.setSat(Boolean.parseBoolean((String) repetition.get("sat")));
                
                valid = dog.addBlockOut(new Block(type,location,new Time(startHours,startMinutes),
                    new Time(endHours,endMinutes), days));
                if(!valid)
                    return dog;
            }
            
            //dog.printBlockOuts();
            //System.out.println();
            
            String courseName;
            String courseNumber;
            for(int i=0;i<courses.size();i++)
            {
                courseName = (String) ((JSONObject) courses.get(i)).get("name");
                courseNumber = (String) ((JSONObject) courses.get(i)).get("number");
                valid = dog.addCourse(courseName+"_"+courseNumber);
                if(!valid)
                    return dog;
            }
            
            //dog.printCourses();
            //System.out.println();
            
            JSONArray course;
            JSONObject section;
            String room;
            String instructor;
            String id;
            String sectionNum;
            ArrayList<String> userCourses = dog.getCourses();
            ArrayList<ArrayList<Section>> allSections = new ArrayList<ArrayList<Section>>();
            
            for(int i=0;i<userCourses.size();i++)
            {
                allSections.add(new ArrayList<Section>());
                course = (JSONArray) sections.get(userCourses.get(i));
                for(int j=0;j<course.size();j++)
                {
                    days = new DaysAvailable(false,false,false,false,false,false,false);
                            
                    section = (JSONObject) course.get(j);
                    
                    room = (String) section.get("room");
                    
                    instructor = (String) section.get("instructor");
                    
                    id = (String) section.get("_id");
                    
                    sectionNum = (String) section.get("section_number");
                    
                    startTime = (JSONObject) section.get("start_time");
                    startHours = ((Long) (startTime.get("hour"))).intValue();
                    startMinutes = ((Long) (startTime.get("minute"))).intValue();
                
                    endTime = (JSONObject) section.get("end_time");
                    endHours = ((Long) (endTime.get("hour"))).intValue();
                    endMinutes = ((Long) (endTime.get("minute"))).intValue();
                
                    days = new DaysAvailable(false,false,false,false,false,false,false);
                    repetition = (JSONObject) section.get("repetition");
                    
                    if(repetition.get("sun") instanceof Boolean)
                        days.setSun((boolean) repetition.get("sun"));
                    else if(repetition.get("sun") instanceof String)
                        days.setSun(Boolean.parseBoolean((String) repetition.get("sun")));
                    
                    if(repetition.get("mon") instanceof Boolean)
                        days.setMon((boolean) repetition.get("mon"));
                    else if(repetition.get("mon") instanceof String)
                        days.setMon(Boolean.parseBoolean((String) repetition.get("mon")));
                    
                    if(repetition.get("tues") instanceof Boolean)
                        days.setTues((boolean) repetition.get("tues"));
                    else if(repetition.get("tues") instanceof String)
                        days.setTues(Boolean.parseBoolean((String) repetition.get("tues")));
                    
                    if(repetition.get("weds") instanceof Boolean)
                        days.setWed((boolean) repetition.get("weds"));
                    else if(repetition.get("weds") instanceof String)
                        days.setWed(Boolean.parseBoolean((String) repetition.get("weds")));
                    
                    if(repetition.get("thurs") instanceof Boolean)
                        days.setThurs((boolean) repetition.get("thurs"));
                    else if(repetition.get("thurs") instanceof String)
                        days.setThurs(Boolean.parseBoolean((String) repetition.get("thurs")));
                    
                    if(repetition.get("fri") instanceof Boolean)
                        days.setFri((boolean) repetition.get("fri"));
                    else if(repetition.get("fri") instanceof String)
                        days.setFri(Boolean.parseBoolean((String) repetition.get("fri")));
                    
                    if(repetition.get("sat") instanceof Boolean)
                        days.setSat((boolean) repetition.get("sat"));
                    else if(repetition.get("sat") instanceof String)
                        days.setSat(Boolean.parseBoolean((String) repetition.get("sat")));
                    
                    allSections.get(i).add(new Section(userCourses.get(i)+"-"+sectionNum, 
                        new Time(startHours,startMinutes), new Time(endHours,endMinutes),
                        days,instructor,room,id));
                }
            }
            valid = dog.setSections(allSections);
            if(!valid)
                return dog;
            
            //dog.printSections(dog.getSections());
            dog.generateSchedules();
            
            return dog;
 
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println(e);
            return null;
        }
    }
    
    public static JSONObject outputFile(User dog, String fileName)
    {   
        JSONObject obj = new JSONObject();
        JSONObject block =new JSONObject();
        Block b;
        Time time;
        JSONObject timeObj;
        String hr;
        String min;
        String courseName;
        String sectionNumber;
        String[] splitString;
        String[] days = {"sunday","monday","tuesday","wednesday","thursday","friday","saturday"};
        JSONArray day = new JSONArray();
        JSONObject schedule = new JSONObject();
        JSONArray schedules = new JSONArray();
        JSONArray sections = new JSONArray();
        
        if(dog==null)
        {
            obj.put("schedules", null);
            obj.put("status","failed");
            obj.put("error","Input file could not be read!");
            try
            {
                FileWriter file = new FileWriter("C:\\Users\\Matthew\\Documents\\out\\"+fileName); 
                file.write(obj.toString());
                System.out.println("what: "+obj.toString());
                System.out.println("Successfully Copied JSON Object to File...");
                System.out.println("\nJSON Object: " + obj);
                file.close();
            }
            catch(Exception e)
            {
                System.out.println(e);
                return null;
            }
        
            return(obj);
        }
        
        ArrayList<ArrayList<ArrayList<Block>>> finalSchedules = dog.getFinalSchedules();
        ArrayList<ArrayList<String>> sectionIDs = dog.getSectionIDs();
        
        if(finalSchedules==null || finalSchedules.size()==0)
        {
            obj.put("schedules", null);
            obj.put("status","failed");
            obj.put("error",dog.getNotification());
        }
        else
        {
            
            for(int i=0;i<finalSchedules.size();i++)
            {
                schedule = new JSONObject();
                sections = new JSONArray();
                for(int s =0;s<sectionIDs.get(i).size();s++)
                {
                    sections.add(sectionIDs.get(i).get(s));
                }
                
                for(int j=0;j<finalSchedules.get(i).size();j++)
                {
                    day = new JSONArray();
                    for(int k=0;k<finalSchedules.get(i).get(j).size() && j<7;k++)
                    {
                        block = new JSONObject();
                        b = finalSchedules.get(i).get(j).get(k);
                        
                        time = b.getStartTime();
                        hr = String.valueOf(time.getHours());
                        min = String.valueOf(time.getMinutes());
                        if(time.getHours()/10==0)
                            hr = "0"+hr;
                        if(time.getMinutes()/10==0)
                            min = "0"+min;
                        
                        timeObj = new JSONObject();
                        timeObj.put("hour",hr);
                        timeObj.put("minute",min);
                        block.put("start_time", timeObj);
                        
                        time = b.getEndTime();
                        hr = String.valueOf(time.getHours());
                        min = String.valueOf(time.getMinutes());
                        if(time.getHours()/10==0)
                            hr = "0"+hr;
                        if(time.getMinutes()/10==0)
                            min = "0"+min;
                        
                        timeObj = new JSONObject();
                        timeObj.put("hour",hr);
                        timeObj.put("minute",min);
                        block.put("end_time", timeObj);
                        
                        block.put("type", b.getType());
                        block.put("location",b.getLocation());
                        
                        if(b instanceof Section)
                        {
                            splitString = ((Section) b).getSectionNum().split("-");
                            if(splitString.length>=3)
                            {
                                courseName = splitString[0];
                                courseName = courseName.replaceAll("_"," ");
                                sectionNumber = splitString[1];
                            }
                            else
                            {
                                courseName=null;
                                sectionNumber = null;
                            }
                            
                            block.put("room",((Section) b).getRoom());
                            block.put("name", courseName);
                            block.put("instructor", ((Section) b).getInstructor());
                            block.put("section",sectionNumber);
                            
                        }   
                        day.add(block);
                    }
                    schedule.put(days[j], day);
                }
                schedule.put("sections",sections);
                schedules.add(schedule);
            }
            
            obj.put("schedules", schedules);
            obj.put("status","complete");
            obj.put("error","none");
        }
        
	try
        {
            FileWriter file = new FileWriter
            ("/Users/wghilliard/PycharmProjects/IMS/scheduler_final/tmp/out/"+fileName);
            file.write(obj.toJSONString());
            System.out.println("Successfully Copied JSON Object to File...");
            System.out.println("\nJSON Object: " + obj);
            file.close();
        }
        catch(Exception e)
        {
            System.out.println(e);
            return null;
        }
        
        return(obj);
    }
}

//Give me a sec
//Sorry that I cannot figure it out yet
