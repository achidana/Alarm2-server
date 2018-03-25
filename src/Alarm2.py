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
	##client.messages.create(to="+19374596097", from_="+12603234126", body="Hello Scott!")
	client.calls.create(to="+19374596097", from_="+12603234126", url="http://45.56.125.90:5000/twiml")
	return "Alarm2 ready!" 

@app.route("/twiml", methods=["GET", "POST"])
def response():
        ##return "Hello Scott"
	##print("A")
	##response = twiml.Response()	
	##print("B")
	##response.say("Hello World!")
	##print("C")
	##print(str(response))
	##print("D")
	##return str(response)
	##return Response(str(response))
	print("A")
	##print(request.form['Body'])
	##message_body = request.form['Body']
	##message_body = request.data
	print("B")
	##print("message_body = " + message_body)
	resp = VoiceResponse()
	print("C")
	##replyText = getReply(message_body)
	##replyText = "It works"
	print("D")
	resp.say("Hi Scott!")
	print("E")
	print("str(resp) = " + str(resp))
	return str(resp)
	##return str(resp)

@app.route("/alarm", methods=["GET"])
def getAllEntries():
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "match_all": {}}})
	return jsonify(res)

@app.route("/token", methods=["GET"])
def getAllTokens():
	res = es.search(index="token", doc_type="doc", body={"query": { "match_all": {}}})
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

@app.route("/alarm/delete", methods=["GET"])
def deleteAlarmIndex():
	es.indices.delete(index="alarm2")
	es.indices.delete(index="token")
	es.indices.create(index="alarm2")
	es.indices.create(index="token")
	return "DELETED"

@app.route("/groupalarm", methods=["POST"])
def createGroupAlarm():
	res = es.index(index="alarm2", doc_type="doc", body=request.data)
	retId = res["_id"]
	return retId 

@app.route("/token", methods=["POST"])
def addToken():
	res = es.index(index="token", doc_type="doc", body=request.data)
	retId = res["_id"]
	return retId 

@app.route("/group", methods=["POST"])
def group():
	res = es.index(index="group", doc_type="doc", body=request.data)
	retId = res["_id"]
	group = json.loads(request.data)
	gList = group["members"]
	user = es.search(index="token", doc_type="doc", body={"query": { "match": {"userId": gList[0] }}})
	registration_id = user["hits"]["hits"][0]["_source"]["token"]
	message_title = "Group Alarm Update"
	message_body = "You have a group alarm update"
	data_message = json.loads(request.data)
	result = push_service.notify_single_device(registration_id=registration_id,
	message_title=message_title, message_body=message_body, data_message=data_message)
	print user
	print result
	return retId 

app.run(host="45.56.125.90", port=5000, threaded=True)
