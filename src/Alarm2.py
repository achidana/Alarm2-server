from flask import Flask, url_for
from flask import jsonify
from elasticsearch import Elasticsearch
from flask.ext.restful import reqparse, request
app = Flask('Alarm2')

es = Elasticsearch()

@app.route("/")
def hello():
    return jsonify({'message': 'Alarm2 ready!'}) 


@app.route("/alarm/byuserid/<userId>", methods=["GET"])
def getUserAlarms(userId):
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	return jsonify(res)

@app.route("/alarm", methods=["POST"])
def createAlarm():
	res = es.index(index="alarm2", doc_type="doc", body=request.data)
	return jsonify({'_id': res["_id"]}) 
