import java.io.*;
import java.util.*;
import java.net.*;

import javax.json.JsonObject;

public class testES {
	public static void main(String[] args) {
		System.out.println("WORKING");
		HttpURLConnection conn = null;
		//JsonObject json;
		try {
			StringBuilder result = new StringBuilder();
			URL url = new URL("http://45.56.125.90:5000/");
			conn = (HttpURLConnection) url.openConnection();
			conn.setRequestMethod("GET");
			BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
			String line;
			while ((line = rd.readLine()) != null) {
				result.append(line);
			}
			rd.close();
			System.out.println(result.toString());
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}
