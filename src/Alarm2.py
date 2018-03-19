from flask import Flask, url_for
from flask import jsonify
from elasticsearch import Elasticsearch
from flask.ext.restful import reqparse, request
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAATKhAVJ4:APA91bGRBWjYDx2z0JH3igYH-WK2tAFm3pTW-8UcuNvW1OUGmPosrUPLo2KsRyKz4Q5_CAJ-iIG8A20a8D7VTvtN5K1Lps9QdrabHiQ2G9Ao-v_YLBUnIUfdwRJxzpSvEoIl9LFOjmw3")

app = Flask('Alarm2')
es = Elasticsearch()


@app.route("/")
def hello():
    #return jsonify({'message': 'Alarm2 ready!'}) 
    registration_id = "c62K8crxcIM:APA91bG4cf6hMv2QmvwdYDbNk8cwSMss-SmI2n99VSluJvyNIfcYXTWazciyW5Ufgj2JgBwq_CpbZhaR7VzGMd1-TeTb0KtGUkqoZH-Ws56pSPamu2KFvjiAjWj2chx58th2vQIv-7AA"
    message_title = "Group Alarm Update"
    message_body = "You have a group alarm update"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)
    print result
    return "Alarm2 ready!" 


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
	es.indices.create(index="alarm2")
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
