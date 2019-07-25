from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.yandex
# collection = db.shop   # Подключиться к конкретной коллекции в БД


def dbLen(db):
    """
    Возвращает количество коллекций в БД
    """
    return db.list_collection_names()

def addRecords2DB(import_id, data):
    """
    Добавляет коллекцию в БД
    """
    collection = db['import_{}'.format(import_id)]
    collection.insert_many(data)
    
    return True

def getAllRecords(import_id):
    """
    Получает коллекцию из БД ?(с определенным import_id)?
    """
    pass