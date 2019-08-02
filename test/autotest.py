import pymongo
import requests
import json

ADRESS = 'http://127.0.0.1:5000/'

def testPOST(json_name,expected_code,if_answer_expected,expected_import_id, description):
    with open(json_name) as json_file:
        data = json.load(json_file)

    response = requests.post('http://127.0.0.1:5000/imports',json=data)
    print(response.status_code)
    assert response.status_code == expected_code, "{}: http error".format(description)
    if if_answer_expected:
        assert json.loads(response.content) == { 'data': {'import_id': expected_import_id} }, "{}: import_id error".format(description)


def testGet1(expected_code, import_id,if_answer_expected, json_name, description):
    response = requests.get('http://127.0.0.1:5000/imports/{}/citizens'.format(import_id))
    assert response.status_code == expected_code, "{}: http error"
    if if_answer_expected:
        with open(json_name) as json_file:
            expected_answer = json.load(json_file)
        assert json.loads(response.content) == expected_answer

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
testGet1(200,1,True,'jsons/big_data.json',"get1 Big data")

myclient.drop_database('yandex')