from flask import Flask, url_for
from flask import jsonify
from elasticsearch import Elasticsearch
from flask.ext.restful import reqparse, request
app = Flask('Alarm2')

es = Elasticsearch()

@app.route("/")
def hello():
    #return jsonify({'message': 'Alarm2 ready!'}) 
    return "a"


@app.route("/alarm/byuserid/<userId>", methods=["GET"])
def getUserAlarms(userId):
	res = es.search(index="alarm2", doc_type="doc", body={"query": { "match": {"userId": userId }}})
	#print("%d documents found" % res['hits']['total'])
	#for doc in res['hits']['hits']:
	#    print("%s) %s" % (doc['_id'], doc['_source']['fname']))
    #return "b"
	#return jsonify({'alarm': 'alarm1'}) 
	return jsonify(res)

@app.route("/alarm", methods=["POST"])
def createAlarm():
	res = es.index(index="alarm2", doc_type="doc", body=request.data)
	#return jsonify(request.body)
	#res = es.getdoc(index="alarm2", doc_type="doc", id)
	#print("%d documents found" % res['hits']['total'])
	#for doc in res['hits']['hits']:
	#    print("%s) %s" % (doc['_id'], doc['_source']['fname']))
    #return "b"
	#return jsonify({'alarm': 'alarm1'}) 
	#return jsonify(res)
	#return jsonify(request.data)
	return jsonify({'_id': res["_id"]}) 

#@app.route("/alarm", methods=["PUT"])
#def updateAlarm():

#@app.route("/alarm", methods=["DELETE"])
#def deleteAlarm():
