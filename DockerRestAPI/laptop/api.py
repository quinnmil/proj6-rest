# Laptop Service
import flask
from flask import Flask, request
from flask_restful import Resource, Api
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


class Laptop(Resource):
    def get(self):
        return {
            'Laptops': ['Mac OS', 'Dell', 
            'Windozzee',
	    'Yet another laptop!',
	    'Yet yet another laptop!'
            ]
        }

class HelloWorld (Resource):
	def get(self):
		return {'value': 'hello world'}

class ListAll (Resource):
    def get(self):
        allTimes = collection.find()
        # app.logger.debug(entries[0])
        result = []
        for entry in allTimes:
            result.append({
                'open' : entry ['open_time'],
                'close': entry ['close_time'],
                'km' : entry ['km']
                })

        return flask.jsonify(result= result)

class ListOpenOnly (Resource):
    def get(self):
        allOpen = collection.find()
        result = []
        for entry in allOpen:
            result.append({
                'open' : entry ['open_time']
                })
        return flask.jsonify(result = result)



class ListClosedOnly (Resource):
       def get(self):
        allClose = collection.find()
        result = []
        for entry in allClose:
            result.append({
                'close' : entry ['close_time']
                })
        return flask.jsonify(result = result)



# Create routes
# Another way, without decorators
api.add_resource(Laptop, '/')
api.add_resource(HelloWorld,'/hi')

api.add_resource(ListAll,'/listAll','/listAll/json')
api.add_resource(ListOpenOnly, '/ListOpenOnly', '/ListOpenOnly/json')
api.add_resource(ListClosedOnly, '/ListClosedOnly','/ListCLosedOnly/json')
# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
