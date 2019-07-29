from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.yandex
# collection = db.shop   # Подключиться к конкретной коллекции в БД


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
    Получает коллекцию из БД ?(с определенным import_id)?
    """
    collection = db['import_{}'.format(import_id)]
    cursor = collection.find({})
    returnedData = [document for document in cursor]
    return returnedData

def changeRecord(import_id, citizen_id):
    """
    Изменяет информацию о житиле и возвращает новую информацию
    """
    pass