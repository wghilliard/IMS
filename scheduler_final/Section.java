/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Matthew
 */
public class Section extends Block {
    
    private String sectionNum;
    private String instructor;
    private String room;
    private String uuID;
    
    public Section(String sectionNum, Time startTime, Time endTime, 
            DaysAvailable days, String instructor, String room,
            String uuID)
        {
            super("class","school",startTime,endTime,days);
            setSectionNum(sectionNum);
            setInstructor(instructor);
            setRoom(room);
            setUuID(uuID);
        }

    public String getInstructor() {
        return instructor;
    }

    public void setInstructor(String instructor) {
        this.instructor = instructor;
    }

    public String getRoom() {
        return room;
    }

    public void setRoom(String room) {
        this.room = room;
    }

    public String getID() {
        return uuID;
    }

    public void setUuID(String uuID) {
        this.uuID = uuID;
    }
    
    public String getSectionNum() {
        return sectionNum;
    }

    public void setSectionNum(String sectionNum) {
        if(sectionNum==null)
            this.sectionNum = "TBA";
        else
            this.sectionNum = sectionNum;
    }
    
    @Override
    public String toString()
    {
        return "{sectionNumber: " +getSectionNum() + ", type: "
                + getType() +", location: " +getLocation() + ", Time: "
                + getStartTime()+ "-"+ getEndTime()+" " +getDays()+"}";
    }
}
