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
##from twilio.twiml.messaging_response import Message, MessagingResponse

push_service = FCMNotification(api_key="AAAATKhAVJ4:APA91bGRBWjYDx2z0JH3igYH-WK2tAFm3pTW-8UcuNvW1OUGmPosrUPLo2KsRyKz4Q5_CAJ-iIG8A20a8D7VTvtN5K1Lps9QdrabHiQ2G9Ao-v_YLBUnIUfdwRJxzpSvEoIl9LFOjmw3")

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

@app.route("/alarm", methods=["GET"])
def getAllEntries():
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "match_all": {}}})
	return jsonify(res)

@app.route("/alarm/byuserid/<userId>", methods=["GET"])
def getUserAlarms(userId):
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	ret = res["hits"]
	return jsonify(ret)

@app.route("/alarm/<_id>", methods=["GET"])
def getAlarm(_id):
	print _id
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "terms": {"_id": [_id]}}})
	print res
	ret = res["hits"]["hits"][0]["_source"]
	#res = es.search(index="alarm2", doc_type="doc", body={"query": { "ids": {"values": [_id]}}})
	return jsonify(ret)

@app.route("/alarm/<_id>", methods=["PUT"])
def updateAlarm(_id):
	res = es.index(index="alarm2", doc_type="doc", id=_id, body=request.data)
	return jsonify(res)

@app.route("/alarm", methods=["POST"])
def createAlarm():
	res = es.index(index="alarm2", doc_type="doc", body=request.data)
	retId = res["_id"]
	return retId 

@app.route("/alarm/<_id>", methods=["DELETE"])
def deleteAlarm(_id):
	res = es.delete(index="alarm2", doc_type="doc", id=_id)
	return jsonify(res)

@app.route("/delete", methods=["GET"])
def deleteAlarmIndex():
	es.indices.delete(index="alarm2")
	es.indices.delete(index="token")
	es.indices.delete(index="group")
	es.indices.create(index="alarm2")
	es.indices.create(index="token")
	es.indices.create(index="group")
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
	res = es.index(index="group", doc_type="doc", body=request.data)
	retId = res["_id"]
	group = json.loads(request.data)
	gList = group["members"]
	for i in range(len(gList)):
	    user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": gList[i] }}})
	    registration_id = user["hits"]["hits"][0]["_source"]["token"]
	    message_title = "New Group Alarm"
	    message_body = "You have a group alarm update"
	    data_message = json.loads(request.data)
	    result = push_service.notify_single_device(registration_id=registration_id,
	    message_title=message_title, message_body=message_body, data_message=data_message)
	return retId

	'''
@app.route("/group/<_id>", methods=["PUT"])
def updateGroupAlarm():
	oldRes = es.search(index="group", doc_type="doc", body={"query": { "terms": {"_id": [_id]}}})
	oldGroup = oldRes["hits"]["hits"][0]["_source"]
	oldGList = oldGroup["members"]
	newRes = es.index(index="group", doc_type="doc", id=_id,  body=request.data)
	newGroup = json.loads(newRes)
	newGList = newGroup["members"]
	for i in range(len(newGList)):
	    userId = newGList[i]
	    user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	    registration_id = user["hits"]["hits"][0]["_source"]["token"]
	    if (any(userId in t for t in oldGList)):
		message_title = "Group Alarm Update"
		message_body = "You have a group alarm update"
		data_message = json.loads(request.data)
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
	    else:
		message_title = "New Group Alarm"
		message_body = "You have a group alarm update"
		data_message = json.loads(request.data)
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
	for i in range(len(oldGList)):
	    userId = newGList[i]
	    user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	    registration_id = user["hits"]["hits"][0]["_source"]["token"]
	    if (not any(userId in t for t in newGList)):
		message_title = "DELETE"
		message_body = "You have a group alarm update"
		data_message = _id
		result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body, data_message=data_message)
	return newRes
	'''

@app.route("/group/<_id>", methods=["DELETE"])
def deleteGroupAlarm():
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "terms": {"_id": [_id]}}})
	print res
	alarm = res["hits"]["hits"][0]["_source"]
	group = json.loads(alarm)
	gList = group["members"]
	for i in range(len(gList)):
	    user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": gList[0] }}})
	    registration_id = user["hits"]["hits"][0]["_source"]["token"]
	    message_title = "DELETE"
	    message_body = "You have a group alarm update"
	    data_message = _id
	    result = push_service.notify_single_device(registration_id=registration_id,
	    message_title=message_title, message_body=message_body, data_message=data_message)
	print _id
	res = es.delete(index="group", doc_type="doc", id=_id)
	return jsonify(res) 

app.run(host="45.56.125.90", port=5000, threaded=True)
