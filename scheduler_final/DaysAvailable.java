/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author Matthew
 */
public class DaysAvailable {
    private boolean mon;
    private boolean tues;
    private boolean wed;
    private boolean thurs;
    private boolean fri;
    private boolean sat;
    private boolean sun;
    
    public DaysAvailable(boolean mon, boolean tues, boolean wed, boolean thurs, boolean fri, boolean sat, boolean sun)
    {
        setMon(mon);
        setTues(tues);
        setWed(wed);
        setThurs(thurs);
        setFri(fri);
        setSat(sat);
        setSun(sun);
    }

    public boolean isMon() {
        return mon;
    }

    public void setMon(boolean mon) {
        this.mon = mon;
    }

    public boolean isTues() {
        return tues;
    }

    public void setTues(boolean tues) {
        this.tues = tues;
    }

    public boolean isWed() {
        return wed;
    }

    public void setWed(boolean wed) {
        this.wed = wed;
    }

    public boolean isThurs() {
        return thurs;
    }

    public void setThurs(boolean thurs) {
        this.thurs = thurs;
    }

    public boolean isFri() {
        return fri;
    }

    public void setFri(boolean fri) {
        this.fri = fri;
    }

    public boolean isSat() {
        return sat;
    }

    public void setSat(boolean sat) {
        this.sat = sat;
    }

    public boolean isSun() {
        return sun;
    }

    public void setSun(boolean sun) {
        this.sun = sun;
    }
    
    public boolean isOnThatDay(int dayNum) // sunday is 0 and saturday is 6
    {
        if(dayNum==0)
            return isSun();
        if(dayNum==1)
            return isMon();
        if(dayNum==2)
            return isTues();
        if(dayNum==3)
            return isWed();
        if(dayNum==4)
            return isThurs();
        if(dayNum==5)
            return isFri();
        if(dayNum==6)
            return isSat();
        return false;
    }
    
    public void setDay(boolean value, int dayNum)
    {
        if(dayNum==0)
            setSun(value);
        if(dayNum==1)
            setMon(value);
        if(dayNum==2)
            setTues(value);
        if(dayNum==3)
            setWed(value);
        if(dayNum==4)
            setThurs(value);
        if(dayNum==5)
            setFri(value);
        if(dayNum==6)
            setSat(value);
    }
    
    public boolean shareSameDay(DaysAvailable block)
    {
        if((this.isMon()&& block.isMon()) ||
                (this.isTues() && block.isTues()) ||
                (this.isWed() && block.isWed()) ||
                (this.isThurs() && block.isThurs()) ||
                (this.isFri() && block.isFri()) ||
                (this.isSat() && block.isSat()) ||
                (this.isSun() && block.isSun()))
            return true;
        return false;
    }
    
    @Override
    public String toString()
    {
        String days="";
        if(isMon())
            days=days+"Mo";
        if(isTues())
            days=days+"Tu";
        if(isWed())
            days=days+"We";
        if(isThurs())
            days=days+"Th";
        if(isFri())
            days=days+"Fr";
        if(isSat())
            days=days+"Sa";
        if(isSun())
            days=days+"Su";
        return days;    
    }
}
