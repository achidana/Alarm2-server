from flask import Flask, url_for
from flask import jsonify
from elasticsearch import Elasticsearch
from flask.ext.restful import reqparse, request
app = Flask('Alarm2')

es = Elasticsearch()

@app.route("/")
def hello():
    return jsonify({'message': 'Alarm2 ready!'}) 


@app.route("/alarm", methods=["GET"])
def getAllEntries():
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "match_all": {}}})
	return jsonify(res)

@app.route("/alarm/byuserid/<userId>", methods=["GET"])
def getUserAlarms(userId):
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	return jsonify(res)

@app.route("/alarm/<_id>", methods=["GET"])
def getAlarm(_id):
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "terms": {"_id": _id}}})
	return jsonify(res)

@app.route("/alarm/<_id>", methods=["PUT"])
def updateAlarm(_id):
	res = es.index(index="alarm2", doc_type="doc", id=_id, body=request.data)
	return jsonify(res)

@app.route("/alarm", methods=["POST"])
def createAlarm():
	res = es.index(index="alarm2", doc_type="doc", body=request.data)
	return jsonify(res)

@app.route("/alarm/<_id>", methods=["DELETE"])
def deleteAlarm(_id):
	res = es.delete(index="alarm2", doc_type="doc", id=_id)
	return jsonify(res)

@app.route("/groupalarm", methods=["POST"])
def createGroupAlarm():
	res = es.index(index="alarm2", doc_type="doc", body=request.data)
	return jsonify({'_id': res["_id"]}) 
