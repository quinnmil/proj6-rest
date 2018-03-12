# Laptop Service
import json
import csv
import flask
from flask import Flask, request, Response
from flask_restful import Resource, Api, reqparse
import pymongo
from pymongo import MongoClient
import sys
import os
import logging

# Instantiate the app
app = flask.Flask(__name__)
api = Api(app)


client = MongoClient('db', 27017)
db = client.tododb
collection = db.control


# Resources 
# ====================
class ListAll (Resource):
	def get(self,top = None):
		top = request.args.get('top', 0, type=int)
		if top is not 0:
			record = getAll(top,True,True)
		else:
			record = getAll(None,True,False)
		return flask.jsonify(result= record)


class ListOpenOnly (Resource):
	def get(self):

		top = request.args.get('top', 0, type=int)
		if top is not 0:
			record = getAll(top,True,False,sortField = "open_time")  
		else:
			record = getAll(None,True,False,sortField = "open_time")		
		return flask.jsonify(result= record)



class ListClosedOnly (Resource):
	def get(self):
		top = request.args.get('top', 0, type=int)

		if top is not 0:
			record = getAll(top,False,True,sortField = "close_time")
		else:
			record = getAll(None,False,True)
		return flask.jsonify(result= record)

class listAllcsv(Resource):
	def get(self):
		top = request.args.get('top', 0, type=int)
		if top is not 0:
			record = getAll(top,True,True)
		else:	
			record = getAll(None,True,True)
		json2csv(record,True,True)
		csvfile = open('data.csv', 'r')
		return Response(csvfile, mimetype='text/csv')


class listOpenOnlycsv(Resource):
	def get(self,):
		top = request.args.get('top', 0, type=int)

		if top is not 0:
			record = getAll(top,True,False,sortField = "open_time")
		else:
			record = getAll(None,True,False,sortField = "open_time")

		json2csv(record,True,False)
		csvfile = open('data.csv', 'r')
		return Response(csvfile, mimetype='text/csv')

class listCloseOnlycsv(Resource):
	def get(self,top = None):
		top = request.args.get('top', 0, type=int)

		if top is not 0:
			record = getAll(top,False,True,sortField = "close_time")
		else:
			record = getAll(None,False,True,sortField = "close_time")
		json2csv(record,False,True)
		csvfile = open('data.csv', 'r')
		return Response(csvfile, mimetype='text/csv')



# Create routes
api.add_resource(ListAll,'/listAll','/listAll/json')
api.add_resource(ListOpenOnly, '/listOpenOnly','/listOpenOnly/json')
api.add_resource(ListClosedOnly, '/listCloseOnly','/listCLoseOnly/json')
api.add_resource(listAllcsv, '/listAll/csv')
api.add_resource(listOpenOnlycsv, '/listOpenOnly/csv')
api.add_resource(listCloseOnlycsv, '/listCloseOnly/csv')

#  functions: 
# ===========================
def getAll(top,isOpen,isClose,sortField = None):
	limit = 20
	sortStr = "open_time"
	if top is not None:
		limit = top
	if sortField is not None:
		sortStr = sortField

	allTimes = collection.find().sort(sortStr, pymongo.ASCENDING).limit(int(limit))
	result = []
	for entry in allTimes:
		if isOpen and isClose:
			result.append({
				'open': entry['open_time'],
				'close': entry['close_time'],
				'km': entry['km']
				})
		elif isOpen:
			result.append({
				'open': entry['open_time'],
				'km': entry['km']
				})
		else:
			result.append({
				'close': entry['close_time'],
				'km': entry['km']
				})
	app.logger.debug(result)
	return result

def json2csv(jsonObj,ifOpen,ifClose):
	obj = jsonObj
	csvfile = open('data.csv', 'w')
	out = csv.writer(csvfile)

	if ifOpen and ifClose:
		out.writerow(['km','open','close'])
		for x in obj:
			out.writerow([x['km'],
					x['open'],
					x['close']])
	elif ifOpen:
		out.writerow(['km','open'])
		for x in obj:
			out.writerow([x['km'],
					x['open']])
	else:
		out.writerow(['km','close'])
		for x in obj:
			out.writerow([x['km'],
					x['close']])	

# Run the application
if __name__ == '__main__':
	app.run(host='0.0.0.0', port=80, debug=True)
