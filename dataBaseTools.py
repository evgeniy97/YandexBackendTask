from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.yandex
collection = db.shop   # Подключиться к конкретной коллекции в БД


def collectionLen(collection):
    """
    Возвращает количество записей в БД
    """
    return collection.estimated_document_count()

def addRecord2DB():
    """
    Добавляет запись в БД
    """
    pass

def getAllRecords():
    """
    Получает все записи из БД ?(с определенным import_id)?
    """
    pass