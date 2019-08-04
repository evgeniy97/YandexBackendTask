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
    Returns the number of collections in the database
    """
    return len(db.list_collection_names())

def addRecords2DB(import_id, data):
    """
    Adds a collection to the database
    data: list if dict
    """
    collection = db['import_{}'.format(import_id)]
    collection.insert_many(data)
    
    return True

def getAllRecords(import_id):
    """
    Gets a collection from the database
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
    Changes resident information and returns new information
    """
    collection = db['import_{}'.format(import_id)]
    data = collection.find_one_and_update(
        {'citizen_id': citizen_id},
        {
            '$set': newData
        }
        ,return_document=ReturnDocument.AFTER
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
