import os 
import numpy as np
from flask import Flask, request, jsonify, Response
from dataBaseTools import dbLen, addRecords2DB, getAllRecords

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, this is implication of yandex backend school's task by Evgeniy Khomutov"


@app.route('/imports',methods=['POST'])
def post():
    if request.method == 'POST':
    # проверяем, что прислали файл НАДО ПРОВЕРИТЬ ЧТО ЭТО JSON
        if 'file' not in request.files:
            return "someting went wrong 1"
    
    ### MagicCode 
    ### Проверить данные 

    ### Получить import_id
    import_id = dbLen + 1
    ### Положить в БД
    
    # Если успешно, то присылаем код 201 и json файл

    return Response(jsonify(
        {
            "data":
            {
                "import_id": import_id
            }
        }
    ), status=201)

@app.route('/imports/<import_id>/citizens/<citizen_id>', methods=['PATCH'])
def patch(import_id, citizen_id):
    """
    Изменяет информацию о жителе в указанном наборе данных
    """
    if request.method == 'PATCH':
    # проверяем, что прислали файл НАДО ПРОВЕРИТЬ ЧТО ЭТО JSON
        if 'file' not in request.files:
            return "someting went wrong 1"
    if  not import_id.is_digital(): return Response(status=400)

    if  not citizen_id.is_digital(): return Response(status=400)

    # Chsnge citizen data then get it
    citizenData = []

    return Response(jsonify(
        {
            "data":
            {
                "import_id": citizenData
            }
        }
    ), status=200)


@app.route('/imports/<import_id>/citizens', methods=['GET'])
def get(import_id):
    """
    Возвращает список всех жителей для указанного набора
    """
    if  not import_id.is_digital(): return Response(status=400)

    return Response(
        jsonify(
            { "data": getAllRecords(import_id) }
            )
    ,status=200)


@app.route('/imports/<import_id>/citizens/birthdays', methods=['GET'])
def getBirthdays(import_id):
    """
    Возвращает жителей и количество подарков, которые они будут покупать
    своим ближайшим родственникам (1-го порядка), сгрупированных по месяцам
    из указанного набора данных
    """
    if  not import_id.is_digital(): return Response(status=400)

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
    if  not import_id.is_digital(): return Response(status=400)

    data = getAllRecords(import_id)

    # Magic function work with data

    return Response(
        jsonify(
            { "data": [] }
            )
    ,status=200)

@app.route('/test_<name>')
def FUNCTION(name):
    return(name)

if __name__ == '__main__':
    app.run()