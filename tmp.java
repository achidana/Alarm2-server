package com.alarm2;

import java.io.*;
import java.util.*;
import java.net.*;
import com.google.gson.*;

/**
 * Hello world!
 *
 */
public class App 
{
    public static void main( String[] args )
    {
	HttpURLConnection conn = null;
	Gson gson = new GsonBuilder().create();
	try {
		// Create Alarm
		StringBuilder result1 = new StringBuilder();
		URL url = new URL("http://45.56.125.90:5000/alarm");
		conn = (HttpURLConnection) url.openConnection();
		conn.setDoOutput(true);
		conn.setDoInput(true);
		conn.setRequestMethod("POST");
		conn.setRequestProperty("Content-Type", "application/json");
		Alarm a = new Alarm();
		a.fname = "Scott";
		a.lname = "Walters";
		a.userId = "9374596097";
		a.days.add("mon");
		a.days.add("tues");
		OutputStreamWriter wr = new OutputStreamWriter(conn.getOutputStream());
		String json = gson.toJson(a);
		System.out.println("json: " + json);
		wr.write(json);
		wr.flush();
		BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		String line = "";
		while((line = rd.readLine()) != null) {
			result1.append(line);
		}
		String res = result1.toString();
		System.out.println("return value: " + res);
		a.esId = res;
		System.out.println(a.toString());
		conn.disconnect();

		System.out.println("BETWEEN\n");

		// Update Alarm
		a.days.add("wed");
		a.days.add("sat");
		StringBuilder result2 = new StringBuilder();
		String urlStr = "http://45.56.125.90:5000/alarm/" + a.esId;
		url = new URL(urlStr);
		conn = (HttpURLConnection) url.openConnection();
		conn.setDoOutput(true);
		conn.setDoInput(true);
		conn.setRequestProperty("Content-Type", "application/json");
		conn.setRequestMethod("PUT");
		wr = new OutputStreamWriter(conn.getOutputStream());
		json = gson.toJson(a);
		System.out.println("json: " + json);
		wr.write(json);
		wr.flush();
		rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		line = "";
		while((line = rd.readLine()) != null) {
			result2.append(line);
		}
		rd.close();
		conn.disconnect();
		res = result2.toString();
		System.out.println("res: " + res);
		//a = gson.fromJson(res, Alarm.class);
		System.out.println("alarm = " + a);

		
		/*
		System.out.println("BETWEEN\n");

		// Get Alarm
		StringBuilder result3 = new StringBuilder();
		url = new URL("http://45.56.125.90:5000/alarm/JQ_evmEBeoIbfpOsn4-P");
		conn = (HttpURLConnection) url.openConnection();
		conn.setRequestMethod("GET");
		rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
		line = "";
		while((line = rd.readLine()) != null) {
			result3.append(line);
		}
		rd.close();
		conn.disconnect();
		res = result3.toString();
		System.out.println("res: " + res);
		a = gson.fromJson(res, Alarm.class);
		System.out.println("alarm = " + a);
		*/
	} catch (Exception e) {
		e.printStackTrace();
	}
        System.out.println( "Hello World!" );
    }
}
