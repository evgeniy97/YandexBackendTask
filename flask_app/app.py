import os 
import numpy as np
from flask import Flask, request, jsonify, Response
from marshmallow import Schema, fields, ValidationError

from dataBaseTools import dbLen, addRecords2DB, getAllRecords, changeRecord, isAvailable, checkCitizenExits
from setting import SERVER_ADRESS
import functional 

app = Flask(__name__)


class CitizenSchema(Schema):
    citizen_id = fields.Integer(required=True, validate=lambda x: x >= 0)
    town = fields.Str(required=True)
    street = fields.Str(required=True)
    building = fields.Str(required=True)
    apartment = fields.Int(required=True,validate=lambda x: x >= 0)
    name = fields.Str(required=True)
    birth_date = fields.DateTime(format='%d.%m.%Y',required=True)
    gender = fields.Str(required=True, validate=lambda x: x in ['male','female']) # male/female
    relatives = fields.List(fields.Int, required=True)

@app.route('/')
def hello():
    return "Hello, this is implication of yandex backend school's task by Evgeniy Khomutov"

@app.route('/imports',methods=['POST'])
def post():
    if not request.is_json: return Response(status=400)
     
    # Get data from request 
    content = request.json
    data = content['citizens']

    try:
        CitizenSchema(many=True).load(data)
    except ValidationError:
        return Response(status=400)

    if not functional.isRelativesCorrect(data):
        return Response(status=400)

    # Get import_id
    import_id = dbLen() + 1
    # Add to DB
    addRecords2DB(import_id,data)

    return jsonify({"data":{"import_id": import_id}}), 201

class CitizenPathSchema(Schema):
    town = fields.Str()
    street = fields.Str()
    building = fields.Str()
    apartment = fields.Int(validate=lambda x: x >= 0) # >0
    name = fields.Str()
    birth_date = fields.DateTime(format='%d.%m.%Y')
    gender = fields.Str(validate=lambda x: x in ['male','female']) # male/female
    relatives = fields.List(fields.Int)

@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def patch(import_id, citizen_id): # TEST
    """
    Change information about current citizens in curren import
    """

    if  not import_id.isdigit(): return Response(status=400)
    if  not citizen_id.isdigit(): return Response(status=400)
    if int(import_id) > dbLen(): return Response(status=400)
    if not checkCitizenExits(import_id,int(citizen_id)): return Response(status=400)

    content = request.json
    if len(content) == 0: return Response(status=400)

    try:
        CitizenPathSchema().load(content)
    except ValidationError:
        return Response(status=400)
    
    # Change citizen data then get it
    citizenData = functional.change(import_id,int(citizen_id),content)

    return jsonify( {"data":citizenData }), 200


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def get(import_id): # +
    """
    Return list of citizens for import_id
    """
    if  not import_id.isdigit(): return Response(status=400)
    if int(import_id) > dbLen(): return Response(status=400)
 
    return jsonify({ "data": getAllRecords(import_id)}), 200


@app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
def getBirthdays(import_id):
    """
    Returns residents and the number of gifts they will buy
    to your immediate family (1st order), grouped by month
    from the specified dataset
    """

    if  not import_id.isdigit(): return Response(status=400)
    if int(import_id) > dbLen(): return Response(status=400)

    responseData = functional.calculatePresents(import_id)

    return jsonify( { "data": responseData } ), 200

@app.route('/imports/<import_id>/towns/stat/percentile/age', methods=['GET'])
def getAgePercentile(import_id):
    """
    Returns city statistics for the specified dataset
    in terms of age: p50, p75, p99, where the number is the percentile value
    """
    if  not import_id.isdigit(): return Response(status=400)
    if int(import_id) > dbLen(): return Response(status=400)

    responseData = functional.calculatePercentileFunctional(import_id)

    return jsonify( { "data": responseData } ) , 200



if __name__ == '__main__':
    if isAvailable():
        app.run()
    else:
        print("Server not available")