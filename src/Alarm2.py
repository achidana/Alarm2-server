from flask import Flask, url_for, request
from flask import jsonify
from elasticsearch import Elasticsearch
from flask.ext.restful import reqparse, request
from pyfcm import FCMNotification
import json
##from bottle import Response
from twilio.rest import Client
from twilio import twiml
from twilio.twiml.voice_response import VoiceResponse, Say
import time
##from twilio.twiml.messaging_response import Message, MessagingResponse

push_service = FCMNotification(api_key="AAAABGjvRZU:APA91bHbi73nAsDBWM5eflhAFNa72Qd9glAFmfotPij-uZBEL-xGEXA7EGsr01pr37cRO_swfAHP7Zi7aOruOAvL53JOob5VnXd06ZfQdqA63o8UyOspGfAa7ZPyCs15bW9-F6F5Hhsq")

app = Flask('Alarm2')
##app.run(threaded=True)
es = Elasticsearch()

account_sid = "ACa6873b79829fb995b9370c799cf83904" 
auth_token = "0525a486a792661745634c026fded00f"
client = Client(account_sid, auth_token)

@app.route("/")
def hello():
	return "Alarm2 ready!" 

@app.route("/text/<phone>/<message>", methods=["GET",  "POST"])
def textFriend(phone, message):
	print phone
	print message
	client.messages.create(to=phone, from_="+12603234126", body=message)
	return "Texting Friend"

@app.route("/call/<phone>/<message>", methods=["GET"])
def callFriend(phone, message):
	phone
	print phone
	print message
	if message.find(" ") != -1:
	    message = message.replace(" ", "%20")
	if message.find("?") != -1:
	    message = message.replace("?", "%3F")
	url_ = "http://45.56.125.90:5000/twiml/call/" + message
	print url_
	client.calls.create(to=phone, from_="+12603234126",url=url_)
	return "Calling Friend"

@app.route("/twiml/call/<message>", methods=["GET", "POST"])
def twimlCall(message):
	print message
	resp = VoiceResponse()
	resp.say(message)
	return str(resp)
	##return str(resp)

@app.route("/alarm/byuserid/<userId>", methods=["GET"])
def getUserAlarms(userId):
	res = es.search(index="alarm", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	ret = res["hits"]
	return jsonify(ret)

@app.route("/alarms", methods=["GET"])
def getAllAlarms():
	res = es.search(index="alarm", doc_type="doc", body={"query": { "match_all": {}}})
	return jsonify(res)

@app.route("/alarm/<_id>", methods=["GET"])
def getAlarm(_id):
	print _id
	res = es.search(index="alarm", doc_type="doc", body={"query": { "terms": {"_id": [_id]}}})
	ret = res["hits"]["hits"][0]["_source"]
	print ret
	#res = es.search(index="alarm", doc_type="doc", body={"query": { "ids": {"values": [_id]}}})
	return jsonify(ret)

@app.route("/alarm/<_id>", methods=["PUT"])
def updateAlarm(_id):
	print _id
	print json.loads(request.data)
	res = es.index(index="alarm", doc_type="doc", id=_id, body=request.data)
	return jsonify(res)

@app.route("/alarm", methods=["POST"])
def createAlarm():
	res = es.index(index="alarm", doc_type="doc", body=request.data)
	retId = res["_id"]
	time.sleep(5)
	alarm = es.search(index="alarm", doc_type="doc", body={"query": { "terms": {"_id": [retId] }}})
	alarm = alarm["hits"]["hits"][0]
	alarm["_source"]["esID"] = retId
	print alarm["_source"]
	res = es.index(index="alarm", doc_type="doc", id=retId,  body=alarm["_source"])
	return retId 

@app.route("/alarm/<_id>", methods=["DELETE"])
def deleteAlarm(_id):
	res = es.delete(index="alarm", doc_type="doc", id=_id)
	return jsonify(res)

@app.route("/times", methods=["GET"])
def getAllTimeAlarms():
	res = es.search(index="time", doc_type="doc", body={"query": { "match_all": {}}})
	return jsonify(res)

@app.route("/time/<_id>", methods=["GET"])
def getTimeAlarm(_id):
	print _id
	res = es.search(index="time", doc_type="doc", body={"query": { "terms": {"_id": [_id]}}})
	ret = res["hits"]["hits"][0]["_source"]
	print ret
	#res = es.search(index="time", doc_type="doc", body={"query": { "ids": {"values": [_id]}}})
	return jsonify(ret)

@app.route("/time/<_id>", methods=["PUT"])
def updateTimeAlarm(_id):
	print _id
	print json.loads(request.data)
	res = es.index(index="time", doc_type="doc", id=_id, body=request.data)
	return jsonify(res)

@app.route("/time", methods=["POST"])
def createTimeAlarm():
	res = es.index(index="time", doc_type="doc", body=request.data)
	retId = res["_id"]
	time.sleep(5)
	alarm = es.search(index="time", doc_type="doc", body={"query": { "terms": {"_id": [retId] }}})
	alarm = alarm["hits"]["hits"][0]
	alarm["_source"]["esID"] = retId
	print alarm["_source"]
	res = es.index(index="time", doc_type="doc", id=retId,  body=alarm["_source"])
	return retId 

@app.route("/time/<_id>", methods=["DELETE"])
def deleteTimeAlarm(_id):
	res = es.delete(index="time", doc_type="doc", id=_id)
	return jsonify(res)

@app.route("/delete", methods=["GET"])
def deleteAllIndex():
	fAlarm = False
	fToken = False
	fGroup = False
	fTime = False
	try: 
	    es.indices.delete(index="alarm")
	    fAlarm = True
	except:
	    pass
	try: 
	    es.indices.delete(index="token")
	    fToken = True
	except:
	    pass
	try: 
	    es.indices.delete(index="group")
	    fGroup = True
	except:
	    pass
	try: 
	    es.indices.delete(index="time")
	    fTime = True
	except:
	    pass
	if fAlarm:
	    es.indices.create(index="alarm")
	if fToken:
	    es.indices.create(index="token")
	if fGroup:
	    es.indices.create(index="group")
	if fTime:
	    es.indices.create(index="time")
	return "DELETED"

@app.route("/token", methods=["POST"])
def addToken():
	res = es.index(index="token", doc_type="doc", body=request.data)
	retId = res["_id"]
	return retId 

@app.route("/tokens", methods=["GET"])
def getAllTokens():
	res = es.search(index="token", doc_type="doc", body={"query": { "match_all": {}}})
	return jsonify(res)

@app.route("/groups", methods=["GET"])
##@crossdomain(origin="*")
def getAllGroups():
	res = es.search(index="group", doc_type="doc", body={"query": { "match_all": {}}})
	return jsonify(res)

@app.route("/group", methods=["POST"])
def createGroupAlarm():
	print json.loads(request.data)
	res = es.index(index="group", doc_type="doc", body=request.data)
	retId = res["_id"]
	time.sleep(5)
	alarm = es.search(index="group", doc_type="doc", body={"query": { "terms": {"_id": [retId] }}})
	alarm = alarm["hits"]["hits"][0]
	alarm["_source"]["esID"] = retId
	print alarm["_source"]
	res = es.index(index="group", doc_type="doc", id=retId,  body=alarm["_source"])
	group = json.loads(request.data)
	gList = group["members"]
	num = len(gList)
	print num
	for i in range(num):
	    print gList[i]
	    user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": gList[i] }}})
	    if (len(user["hits"]["hits"])):
		registration_id = user["hits"]["hits"][0]["_source"]["token"]
		print registration_id
		message_title = "NEW"
		message_body = "You have a group alarm update"
		data_message = alarm["_source"]
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
		print result
	return retId

@app.route("/group/<_id>", methods=["PUT"])
def updateGroupAlarm(_id):
	oldAlarm = es.search(index="group", doc_type="doc", body={"query": { "terms": {"_id": [_id]}}})
	print oldAlarm["hits"]["hits"][0]
	oldGroup = oldAlarm["hits"]["hits"][0]["_source"]
	oldGList = oldGroup["members"]
	newRes = es.index(index="group", doc_type="doc", id=_id,  body=request.data)
	time.sleep(3)
	newAlarm = es.search(index="group", doc_type="doc", body={"query": { "terms": {"_id": [_id]}}})
	print newAlarm["hits"]["hits"][0]
	newGroup = newAlarm["hits"]["hits"][0]["_source"]
	newGList = newGroup["members"]
	for i in range(len(newGList)):
	    userId = newGList[i]
	    user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	    if (len(user["hits"]["hits"])):
		registration_id = user["hits"]["hits"][0]["_source"]["token"]
		if (any(userId in t for t in oldGList)):
		    message_title = "UPDATE"
		    message_body = "You have a group alarm update"
		    data_message = json.loads(request.data)
		    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
		else:
		    message_title = "NEW"
		    message_body = "You have a group alarm update"
		    data_message = json.loads(request.data)
		    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
	for i in range(len(oldGList)):
	    userId = oldGList[i]
	    user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	    registration_id = user["hits"]["hits"][0]["_source"]["token"]
	    if (not(any(userId in t for t in newGList))):
		message_title = "DELETE"
		message_body = "You have a group alarm update"
		data_message = json.loads(request.data)
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
	return jsonify(newRes)

@app.route("/group/<_id>", methods=["DELETE"])
def deleteGroupAlarm(_id):
	res = es.search(index="group", doc_type="doc", body={"query": { "terms": {"_id": [_id]}}})
	print res
	alarm = res["hits"]["hits"][0]["_source"]
	group = json.loads(alarm)
	gList = group["members"]
	for i in range(len(gList)):
	    user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": gList[0] }}})
	    if (len(user["hits"]["hits"])):
		registration_id = user["hits"]["hits"][0]["_source"]["token"]
		message_title = "DELETE"
		message_body = "You have a group alarm update"
		data_message = group 
		result = push_service.notify_single_device(registration_id=registration_id,
		message_title=message_title, message_body=message_body, data_message=data_message)
	print _id
	res = es.delete(index="group", doc_type="doc", id=_id)
	return jsonify(res) 

app.run(host="45.56.125.90", port=5000, threaded=True)
