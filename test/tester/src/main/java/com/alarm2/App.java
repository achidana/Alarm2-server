package com.alarm2;

import java.io.*;
import java.util.*;
import java.net.*;
import com.google.gson.*;


public class App {

    public void prompt() {
	    Scanner s = new Scanner(System.in);
	    Gson gson = new GsonBuilder().create();
	    StringBuilder result;
	    URL url;
	    HttpURLConnection conn;
	    OutputStreamWriter wr;
	    String json;
	    BufferedReader rd;
	    String line;
	    String res;


	    Alarm alarm;
	    String name;
	    String esId;
	    String userId;
	    String days;
	    String[] dArr;
	    int hour;
	    int minute;
	    System.out.println();
	    System.out.println("1: Create Alarm 2: Update Alarm 3: Get Alarm 4: Delete Alarm 5: Get Alarms By ID 6: Reset DB");
	    System.out.print("Enter Call Type: ");
	    int call = s.nextInt();
	    s.nextLine();
		switch (call) {
			case 1:
				alarm = new Alarm();
				System.out.print("Enter name: ");
				name = s.nextLine();
				alarm.setName(name);
				System.out.print("Enter userId: ");
				userId = s.nextLine();
				alarm.setUserId(userId);
				System.out.print("Enter days: ");
				days = s.nextLine();
				dArr = days.split(",");
				for (int i = 0; i < dArr.length; i++) {
					alarm.addDay(dArr[i]);
				}
				System.out.print("Enter hour: ");
				hour = s.nextInt();
				alarm.setHour(hour);
				s.nextLine();
				System.out.print("Enter minute: ");
				minute = s.nextInt();
				alarm.setMinute(minute);
				s.nextLine();

				//Add to Elasticsearch
				try {
				    result = new StringBuilder();
				    url = new URL("http://45.56.125.90:5000/alarm");
				    conn = (HttpURLConnection) url.openConnection();
				    conn.setDoOutput(true);
				    conn.setDoInput(true);
				    conn.setRequestMethod("POST");
				    conn.setRequestProperty("Content-Type", "application/json");
				    wr = new OutputStreamWriter(conn.getOutputStream());
				    json = gson.toJson(alarm);
				    wr.write(json);
				    wr.flush();
				    rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
				    line = "";
				    while((line = rd.readLine()) != null) {
					    result.append(line);
				    }
				    res = result.toString();
				    System.out.println("return value: " + res);
				    alarm.setEsId(res);
				    System.out.println(alarm.toString());
				    conn.disconnect();
				} catch (Exception e) {
				    e.printStackTrace();
				}
				prompt();
				break;
			case 2:
				alarm = new Alarm();
				System.out.print("Enter Es ID: ");
				esId = s.nextLine();
				alarm.setEsId(esId);
				System.out.print("Enter name: ");
				name = s.nextLine();
				alarm.setName(name);
				System.out.print("Enter userId: ");
				userId = s.nextLine();
				alarm.setUserId(userId);
				System.out.print("Enter days: ");
				days = s.nextLine();
				dArr = days.split(",");
				for (int i = 0; i < dArr.length; i++) {
					alarm.addDay(dArr[i]);
				}
				System.out.print("Enter hour: ");
				hour = s.nextInt();
				alarm.setHour(hour);
				System.out.print("Enter minute: ");
				minute = s.nextInt();
				alarm.setMinute(minute);
				s.nextLine();

				//Update to Elasticsearch
				try {
				    result = new StringBuilder();
				    url = new URL("http://45.56.125.90:5000/alarm/" + alarm.esId);
				    conn = (HttpURLConnection) url.openConnection();
				    conn.setDoOutput(true);
				    conn.setDoInput(true);
				    conn.setRequestMethod("PUT");
				    conn.setRequestProperty("Content-Type", "application/json");
				    wr = new OutputStreamWriter(conn.getOutputStream());
				    json = gson.toJson(alarm);
				    wr.write(json);
				    wr.flush();
				    rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
				    line = "";
				    while((line = rd.readLine()) != null) {
					    result.append(line);
				    }
				    res = result.toString();
				    System.out.println("return value: " + res);
				    System.out.println(alarm.toString());
				    conn.disconnect();
				} catch (Exception e) {
				    e.printStackTrace();
				}
				prompt();
				break;
			case 3:
				System.out.print("Enter Elasticsearch ID: " );
				esId = s.nextLine();
				alarm = null;
				try {
				    result = new StringBuilder();
				    url = new URL("http://45.56.125.90:5000/alarm/" + esId);
				    conn = (HttpURLConnection) url.openConnection();
				    conn.setRequestMethod("GET");
				    rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
				    line = "";
				    while((line = rd.readLine()) != null) {
					    result.append(line);
				    }
				    res = result.toString();
				    System.out.println("return value: " + res);
					alarm = gson.fromJson(res, Alarm.class);
				    System.out.println(alarm.toString());
				    conn.disconnect();
				} catch (Exception e) {
				    e.printStackTrace();
				}
				prompt();
				break;
			case 4:
				System.out.print("Enter Elasticsearch ID: " );
				esId = s.nextLine();
				try {
				    result = new StringBuilder();
				    url = new URL("http://45.56.125.90:5000/alarm/" + esId);
				    conn = (HttpURLConnection) url.openConnection();
				    conn.setRequestMethod("DELETE");
				    rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
				    line = "";
				    while((line = rd.readLine()) != null) {
					    result.append(line);
				    }
				    res = result.toString();
				    System.out.println("return value: " + res);
				    conn.disconnect();
				} catch (Exception e) {
				    e.printStackTrace();
				}
				prompt();
				break;
			case 5:
				System.out.print("Enter User ID: " );
				userId = s.nextLine();
				try {
				    result = new StringBuilder();
				    url = new URL("http://45.56.125.90:5000/alarm/byuserid/" + userId);
				    conn = (HttpURLConnection) url.openConnection();
				    conn.setRequestMethod("GET");
				    rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
				    line = "";
				    while((line = rd.readLine()) != null) {
					    result.append(line);
				    }
				    res = result.toString();
				    System.out.println("return value: " + res);
				    Hits hits = gson.fromJson(res, Hits.class);
				    System.out.println("Hits: " + hits.hits);
					/*
					for (int i = 0; i < hits.hits.size(); i++) {
						String h = hits.hits.get(i).toString();
						Hit hit = gson.fromJson(h, Hit.class);
						String a = hit._source.toString();
						alarm = gson.fromJson(a, Alarm.class);
						System.out.println("Alarm " + i + ": " + alarm.toString());
					}	
					*/
				    conn.disconnect();
				} catch (Exception e) {
				    e.printStackTrace();
				}
				prompt();
				break;
			case 6:
				try {
				    result = new StringBuilder();
				    url = new URL("http://45.56.125.90:5000/alarm/delete");
				    conn = (HttpURLConnection) url.openConnection();
				    conn.setRequestMethod("GET");
				    rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
				    line = "";
				    while((line = rd.readLine()) != null) {
					    result.append(line);
				    }
				    res = result.toString();
				    System.out.println("return value: " + res);
				    conn.disconnect();
				} catch (Exception e) {
				    e.printStackTrace();
				}
				prompt();
				break;
			default:
				System.out.println(call);
				prompt();
				break;
		}
    }

    public static void main( String[] args ) {	
		App app = new App();
		app.prompt();
    }
}
