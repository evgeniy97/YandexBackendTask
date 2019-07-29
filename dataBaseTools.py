from pymongo import MongoClient
from pymongo.collection import ReturnDocument

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