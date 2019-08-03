import pymongo
import requests
import json

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.collection import ReturnDocument

ADRESS = 'http://127.0.0.1:5000/'

def getRecord(import_id, citizen_id):
    client = MongoClient("mongodb://localhost:27017")
    db = client.yandex
    collection = db['import_{}'.format(import_id)]
    data = collection.find_one({'citizen_id': int(citizen_id)})
    data.pop('_id',None)
    return data
        
def testPOST(json_name,expected_code,if_answer_expected,expected_import_id, description):
    with open(json_name) as json_file:
        data = json.load(json_file)

    response = requests.post('http://127.0.0.1:5000/imports',json=data)
    print(response.status_code)
    assert response.status_code == expected_code, "{}: http error".format(description)
    if if_answer_expected:
        assert json.loads(response.content) == { 'data': {'import_id': expected_import_id} }, "{}: import_id error".format(description)

def testPath(expected_code, import_id, citizen_id, newData,
        if_answer_expected, json_name, description,
        relativesTest = False, relativesJson = None, relativesID = None):
    response = requests.patch(
        "http://127.0.0.1:5000/imports/{}/citizens/{}".format(import_id, citizen_id),json=newData)
    print(response.status_code)
    assert response.status_code == expected_code, "{}: http error".format(description)
    if if_answer_expected:
        with open(json_name) as json_file:
            expected_answer = json.load(json_file)
        assert json.loads(response.content)['data'] == expected_answer, "{}: data error".format(description)
    if relativesTest:
        for json_relative, relativeID in zip(relativesJson, relativesID):
            with open(json_relative) as f:
                expected_relative_answer = json.load(f)
            
            gottenData = getRecord(import_id,relativeID)
            assert expected_relative_answer == gottenData, "{}: relative {} error".format(description, relativeID)


def testGet1(expected_code, import_id,if_answer_expected, json_name, description):
    response = requests.get('http://127.0.0.1:5000/imports/{}/citizens'.format(import_id))
    print(response.status_code)
    assert response.status_code == expected_code, "{}: http error".format(description)
    if if_answer_expected:
        with open(json_name) as json_file:
            expected_answer = json.load(json_file)
        assert json.loads(response.content)['data'] == expected_answer['citizens'], "{}: data error".format(description)

def testGet2(expected_code,import_id,if_answer_expected, json_name, description):
    response = requests.get('http://127.0.0.1:5000/imports/{}/citizens/birthdays'.format(import_id))
    print(response.status_code)
    assert response.status_code == expected_code, "{}: http error".format(description)
    if if_answer_expected:
        with open(json_name) as json_file:
            expected_answer = json.load(json_file)
        assert json.loads(response.content) == expected_answer, "{}: data error".format(description)

def testGet3(expected_code,import_id,if_answer_expected, json_name, description):
    response = requests.get('http://127.0.0.1:5000/imports/{}/towns/stat/percentile/age'.format(import_id))
    print(response.status_code)
    assert response.status_code == expected_code, "{}: http error".format(description)
    if if_answer_expected:
        with open(json_name) as json_file:
            expected_answer = json.load(json_file)
        assert json.loads(response.content) == expected_answer, "{}: data error".format(description)


# Сбросили database, чтобы провести тесты
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
myclient.drop_database('yandex')

# content TEST

response = requests.get(ADRESS)
assert response.status_code == 200, "Basic GET: error"

# POST test

# Хороший запрос

testPOST('jsons/good_2.json',201,True,1,"Basic POST 2 good request")
testPOST('jsons/good_selfrelate.json',201,True,2,"Basic POST 2 self relate request")
testPOST('jsons/bad_not_all.json',400,False,None,"Basic POST 2 not all request")
testPOST('jsons/bad_relatives_2.json',400,False,None,"Basic POST 2 bad relative request")
testPOST('jsons/bad_type.json',400,False,None,"Basic POST 2 bad type request")
testPOST('jsons/big_data.json',201,True,3,"Big request")

testGet1(200,1,True,'jsons/good_2.json',"get1 Basic 2")
testGet1(400,10,False,None,"get2 Basic bad request")
testGet1(200,3,True,'jsons/big_data.json',"get1 Big data")

testGet2(400,10,False, None,"import_id > len ")
testGet2(400,'Lkd', False, None, "bad import_id")
testGet2(200,1,True,"jsons/birthdays1.json","small data")
testGet2(200,2,True,"jsons/birthdays2.json","small data 2")
testGet2(200,3,True,"jsons/birthdays3.json","big data")

testGet3(400,10,False, None,"import_id > len ")
testGet3(400,'Lkd', False, None, "bad import_id")
testGet3(200,1,True,"jsons/age1.json","small data")
testGet3(200,2,True,"jsons/age2.json","small data 2")
testGet3(200,3,True,"jsons/age3.json","big data")

testPath(400,1,10,{},False,None,"empty")
testPath(400,1,10,{"cat": True},False,None, "bad data")
testPath(400,3,10,{"citizen_id": 10000000},False,None, "citizen_id change")
testPath(400,3,10,{"birth_date":"12.13.2000"},False,None, "incorrect date")
testPath(400,3,10,{"gender": 1},False, None, "bad data type")
testPath(400,3,10000000,{"name": "Ivan"},False,None, "citizen not exist")
testPath(400,19,1,{"name": "Ivan"}, False, None, "import_id not exists")
testPath(400,3,10, [{"name": "Ivan"}, {"Name": "Vasya"}], False, None, "Bad type: list")

testPath(200,3,2,{"name": "Ivan"},True,"jsons/path1.json","name change test")
testPath(200,3,2,{"birth_date": "10.07.1997"},True,"jsons/path2.json","date change")
testPath(200,3,2,{"relatives": [2]}, True, "jsons/path3.json","good_selfrelate")

testPath(200,3,3,{"relatives": [4]},True,"jsons/path4.json","add relative",
        True,["jsons/pathrelative1.json"],[4])
testPath(200,3,3,{"relatives": [4,5]},True,"jsons/path5.json","add relative",
        True,["jsons/pathrelative1.json","jsons/pathrelative2.json"],[4,5])
testPath(200,3,4,{"relatives": []},True,"jsons/path6.json","delete relative",
        True,["jsons/pathrelative3.json"],[3])

myclient.drop_database('yandex')