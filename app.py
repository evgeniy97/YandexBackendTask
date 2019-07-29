import os 
import numpy as np
from flask import Flask, request, jsonify, Response
from marshmallow import Schema, fields, ValidationError
from dataBaseTools import dbLen, addRecords2DB, getAllRecords

app = Flask(__name__)


class CitizenSchema(Schema):
    citizen_id = fields.Integer(required=True, validate=lambda x: x >= 0) # Добавить проверку на уникальность
    town = fields.Str(required=True)
    street = fields.Str(required=True)
    building = fields.Str(required=True)
    apartment = fields.Int(required=True,validate=lambda x: x >= 0) # >0
    name = fields.Str(required=True)
    birth_day = fields.DateTime(format='%d.%m.%Y',required=True)
    gender = fields.Str(required=True, validate=lambda x: x in ['male','female']) # male/female
    relatives = fields.List(fields.Int, required=True)


@app.route('/')
def hello():
    return "Hello, this is implication of yandex backend school's task by Evgeniy Khomutov"


@app.route('/imports',methods=['POST'])
def post():
    #if request.method == 'POST':
    # проверяем, что прислали файл НАДО ПРОВЕРИТЬ ЧТО ЭТО JSON
    #    if 'file' not in request.files:
    #        return Response(status=400)
    
    ### MagicCode 
    # Получить данные из запроса 
    content = request.json
    data = content['citizens']
    # Добавить проверку поля родстенники
    try:
        CitizenSchema(many=True).load(data)
    except ValidationError as err:
        print(err.messages)
        return Response(status=400)

    ### Получить import_id
    import_id = dbLen() + 1
    ### Положить в БД
    addRecords2DB(import_id,data)

    # Если успешно, то присылаем код 201 и json файл
    return Response(
        {"data":{"import_id": import_id}}
    , status=201)



@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def patch(import_id, citizen_id):
    """
    Изменяет информацию о жителе в указанном наборе данных
    """
    #if request.method == 'PATCH':
    # проверяем, что прислали файл НАДО ПРОВЕРИТЬ ЧТО ЭТО JSON
    #    if 'file' not in request.files:
    #        return "someting went wrong 1"
    if  not import_id.isdigit(): return Response(status=400)

    if  not citizen_id.isdigit(): return Response(status=400)

    # Chsnge citizen data then get it
    citizenData = []

    return Response(jsonify(
        {
            "data":
            {
                citizenData
            }
        }
    ), status=200)


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def get(import_id):
    """
    Возвращает список всех жителей для указанного набора
    """
    if  not import_id.isdigit(): return Response(status=400)

    limit = dbLen()
    if int(import_id) >= limit: Response(status=400) # Не работает

    return Response(
            { "data": getAllRecords(import_id) }
    ,status=200)


@app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
def getBirthdays(import_id):
    """
    Возвращает жителей и количество подарков, которые они будут покупать
    своим ближайшим родственникам (1-го порядка), сгрупированных по месяцам
    из указанного набора данных
    """
    if  not import_id.isdigit(): return Response(status=400)

    data = getAllRecords(import_id)

    # Magic function work with data

    return Response(
        jsonify(
            { "data": [] }
            )
    ,status=200)

@app.route('/imports/<import_id>/towns/stat/percentile/age', methods=['GET'])
def getAgePercentile(import_id):
    """
    Возвращает статистику по городам для указанного набора данных
    в разрезе возраста жителец: p50, p75, p99, где число - это значение перцентиля
    """
    if  not import_id.isdigit(): return Response(status=400)

    data = getAllRecords(import_id)

    # Magic function work with data

    return Response(
        jsonify(
            { "data": [] }
            )
    ,status=200)

if __name__ == '__main__':
    app.run()