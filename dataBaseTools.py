from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from pymongo.collection import ReturnDocument
from setting import MONGODB_ADRESS

# Check if db available

client = MongoClient(MONGODB_ADRESS)
db = client.yandex

def isAvailable():
    client = MongoClient(MONGODB_ADRESS,serverSelectionTimeoutMS=1)
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return True
    except ConnectionFailure:
        print("Server not available")
        return False


def dbLen():
    """
    Возвращает количество коллекций в БД
    """
    return len(db.list_collection_names())

def addRecords2DB(import_id, data):
    """
    Добавляет коллекцию в БД
    data: list if dict
    """
    collection = db['import_{}'.format(import_id)]
    collection.insert_many(data)
    
    return True

def getAllRecords(import_id):
    """
    Получает коллекцию из БД
    """
    collection = db['import_{}'.format(import_id)]
    cursor = collection.find({})
    returnedData = [document for document in cursor]
    for doc in returnedData:
        doc.pop('_id',None)
    return returnedData

def changeRecord(import_id, citizen_id, newData):
    """
    newData: dict
    Изменяет информацию о житиле и возвращает новую информацию
    """
    collection = db['import_{}'.format(import_id)]
    data = collection.find_one_and_update(
        {'citizen_id': citizen_id}, # ключ, по которому меняем
        {
            '$set': newData
        }
        ,return_document=ReturnDocument.AFTER # вернуть модифицированный вариант
    )
    data.pop('_id',None)
    return data

def getRecord(import_id, citizen_id):
    collection = db['import_{}'.format(import_id)]
    data = collection.find_one({'citizen_id': int(citizen_id)})
    data.pop('_id',None)
    return data

def checkCitizenExits(import_id, citizen_id):
    collection = db['import_{}'.format(import_id)]
    data = collection.find_one({'citizen_id': int(citizen_id)})
    return bool(data)
