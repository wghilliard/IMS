/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Matthew
 */
public class Block {
    private String type;
    private String location;
    private Time startTime;
    private Time endTime;
    private DaysAvailable days;
    
    public Block(String type, String location, Time startTime, Time endTime, 
            DaysAvailable days)
    {
        setType(type);
        setLocation(location);
        setStartTimeAndEndTime(startTime,endTime);
        setDays(days);
    }

    public void setType(String type) {
        if(type.compareTo("study")==0 || type.compareTo("work")==0 || type.compareTo("sleep")==0 ||
                type.compareTo("commute")==0 || type.compareTo("class")==0 || type.compareTo("other")==0)
            this.type = type;
        else
            this.type = "other";
    }

    public void setLocation(String location) {
        if(this.type.compareTo("work")==0)
            this.location = "work";
        else if(this.type.compareTo("class")==0)
            this.location = "school";
        else if(location.compareTo("school")==0 || location.compareTo("work")==0 ||
                location.compareTo("home")==0 )
            this.location = new String(location);
        else
            this.location = "home";
    }

    public void setStartTimeAndEndTime(Time startTime, Time endTime)
    {
        if(startTime == null || endTime == null)
        {
            this.startTime = new Time(0,0);
            this.endTime = new Time(0,1);
        }
        else if((endTime.getHours()==0 && endTime.getMinutes()==0) ||
                startTime.lessThan(endTime))
        {
            this.startTime = new Time(startTime.getHours(),startTime.getMinutes());
            this.endTime = new Time(endTime.getHours(),endTime.getMinutes());
        }
        else
        {
            this.startTime = new Time(0,0);
            this.endTime = new Time(0,1);
        }
    }

    public void setDays(DaysAvailable days) {
        if(days==null)
            this.days = new DaysAvailable(false,false,false,false,false,false,false);
        else
            this.days = days;
    }

    public DaysAvailable getDays() {
        return days;
    }

    public String getType() {
        return type;
    }

    public String getLocation() {
        return location;
    }

    public Time getStartTime() {
        return startTime;
    }

    public Time getEndTime() {
        return endTime;
    }
    
    
    public boolean checkNoConflicts(Block object)
    {
        if(object==null || this == null)
        {
            System.out.println("darn");
            return false;
        }
        if(this.getDays().shareSameDay(object.getDays()))
        {
            if((this.endTime.getHours()==0 && this.endTime.getMinutes()==0) &&
                    (object.endTime.getHours()==0 && object.endTime.getMinutes()==0))
            {
                return false;
            }
            if(this.endTime.getHours()==0 && this.endTime.getMinutes()==0)
            {
                if(this.startTime.lessThan(object.startTime) ||
                        this.startTime.lessThan(object.endTime))
                    return false;
            }
            if(object.endTime.getHours()==0 && object.endTime.getMinutes()==0)
            {
                if(object.startTime.lessThan(this.startTime) ||
                        object.startTime.lessThan(this.endTime))
                    return false;
            }
            else if((this.startTime.lessThanOrEqual(object.startTime) &&
                object.endTime.lessThanOrEqual(this.endTime)) ||
                        
                (object.startTime.lessThanOrEqual(this.startTime) &&
                this.endTime.lessThanOrEqual(object.endTime)) ||
                        
                (object.startTime.lessThan(this.startTime) &&
                object.endTime.lessThan(this.endTime) &&
                this.startTime.lessThan(object.endTime)) ||
                        
                (this.startTime.lessThan(object.startTime) &&
                this.endTime.lessThan(object.endTime) &&
                object.startTime.lessThan(this.endTime)))
            {
                //System.out.println("eh");
                return false;
            }
        }
        return true;
    }
    
    @Override
    public String toString()
    {
        return "{type: " + getType() +", location: " +getLocation() + ", Time: "
                + getStartTime() + "-" + getEndTime()+" "+getDays()+"}";
    }
}

