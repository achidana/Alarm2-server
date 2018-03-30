package com.alarm2;

import java.util.ArrayList;

public class Alarm { 
	public String name;
	public String userId;
	public String esId;
	public int hour;
	public int minute;
	public ArrayList<String> days = new ArrayList<String>();

	public void setName(String str) {
		this.name = str;
	}
	public void setUserId(String str) {
		this.userId = str;
	}
	public void setEsId(String str) {
		this.esId = str;
	}
	public void setHour(int hr) {
		this.hour = hr;
	}
	public void setMinute(int min) {
		this.minute = min;
	}
	public void addDay(String str) {
		this.days.add(str);
	}

	@Override
	public String toString() {
		return "ElasticId: " + esId + "\nName: " + name + "\nUser ID: " + userId + "\nDays: " + days + "\nHour: " + hour + "\nMinute: " + minute; 
	}
}
