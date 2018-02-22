package com.alarm2;

import java.util.ArrayList;

public class Alarm { 
	public String fname;
	public String lname;
	public String userId;
	public String esId;
	public ArrayList<String> days = new ArrayList<String>();

	@Override
	public String toString() {
		return esId + "\n" + fname + " " + lname + " : " + userId + " : " + days; 
	}
}
