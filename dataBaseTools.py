from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client.yandex

# table =  # Подключиться к конкретной коллекции в БД

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