from datetime import datetime, date
import numpy as np

from dataBaseTools import dbLen, addRecords2DB, getAllRecords, changeRecord 

def minMax(a,b):
    return (min(a,b), max(a,b))

class Relatives(object):
    def __init__(self):
        self.open_relate = set()

    def add(self, person_id_1,person_id_2):
        if person_id_1 == person_id_2:
            return 

        rightPair = minMax(person_id_1,person_id_2)
        if rightPair in self.open_relate:
            self.open_relate.remove(rightPair)
        else:
            self.open_relate.add(rightPair)
        pass
    
    def is_opened(self):
        return len(self.open_relate) == 0




def isRelativesCorrect(data):
    """
    Получает на вход список житилей, смотрит на корректность
    родственных связей. Проходимся по всем жителям и добавляем пару 
    (my_id, my_relatives_id) в список unclosed_id, если такой пары в списке нет.
    Если такая пара есть, то удаляем ее из списка. Если my_id == my_relatives_id,
    то ничего не делаем
    """
    unclosed_id = Relatives()
    for person in data:
        for relative_id in person["relatives"]:
            unclosed_id.add(person['citizen_id'], relative_id)
    return unclosed_id.is_opened() == False

def calculateAge(birthDate):
    """
    Возвращает int: возраст жителя
    """
    date_of_birth = datetime.strptime(birthDate, "%d.%m.%Y")
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


def getCitizen(import_id, citizen_id): #TEST
    return changeRecord(import_id,int(citizen_id),{}) # Лучше написать функцию, которая просто возрасщает запись

def getCitizenMonth(import_id, citizen_id):
    return str(int(getCitizen(import_id, citizen_id)['birth_date'][3:5])) # str(int('01')) -> '1'

def calculatePresents(import_id): # TEST
    data = getAllRecords(import_id)
    
    returnedMonth = {}
    for i in range(1,13):
        returnedMonth[str(i)] = []
    
    for person in data:
        if len(person['relatives']) == 0: pass
        relativesMonth = {}
        for relative_id in person['relatives']:
            month = getCitizenMonth(import_id, relative_id)
            if month in relativesMonth:
                relativesMonth[month] += 1
            else:
                relativesMonth[month] = 1
        
        # Раскидать этого person по месяцам
        for month, number in relativesMonth.items():
            returnedMonth[month].add(
                {
                    "citizen_id": person['citizen_id'],
                    "presents": number
                }
            )

    return returnedMonth

def calculatePercentile(city_name, ages):
    return {
        "town": city_name,
        "p50": np.percentile(ages,50,interpolation='linear'),
        "p75": np.percentile(ages,75,interpolation='linear'),
        "p99": np.percentile(ages,99,interpolation='linear')
    }