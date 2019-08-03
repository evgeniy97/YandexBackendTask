from datetime import datetime, date
import numpy as np

from dataBaseTools import dbLen, addRecords2DB, getAllRecords, changeRecord, getRecord

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
    
    def is_opened(self):
        return len(self.open_relate) != 0




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
    return getRecord(import_id,int(citizen_id)) # Лучше написать функцию, которая просто возрасщает запись

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
            returnedMonth[month].append(
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

def calculatePercentileFunctional(import_id):
    data = getAllRecords(import_id)

    agesPerTowns = {}

    for person in data:
        if person['town'] in agesPerTowns:
            agesPerTowns[person['town']].append(calculateAge(person['birth_date']))
        else:
            agesPerTowns[person['town']] = [calculateAge(person['birth_date'])]

    responseData = [calculatePercentile(city,agesPerTowns[city]) for city in agesPerTowns.keys()]
    return responseData

def change(import_id,citizen_id, content):
    citizen_id = int(citizen_id)
    if not 'relatives' in content:
        return changeRecord(import_id,citizen_id,content)
    else:
        new_relatives = content.pop('relatives')
        if len(content) != 0:
            data = changeRecord(import_id,citizen_id,content)
        else:
            data = getRecord(import_id,citizen_id)
            
        old_relatives = data['relatives']

        # Этим циклом добавляем новые свзяи
        for relative_id in new_relatives:
            if not relative_id in old_relatives:
                """
                1) Получим данные этого жителя, возьмем из них его родственников
                2) Добавим текущего жителя в список
                3) Обновим список родственников
                """
                otherCitizenDataRelatives = getRecord(import_id,relative_id)['relatives']
                otherCitizenDataRelatives.append(citizen_id)
                changeRecord(import_id,relative_id,{'relatives': otherCitizenDataRelatives})
        
        # Этим циклом удаляем старые связи
        for relative_id in old_relatives:
            if not relative_id in new_relatives:
                """
                1) Получим данные этого жителя, возьмем из них его родственников
                2) Удалим текущего жителя в список
                3) Обновим список родственников
                """
                otherCitizenDataRelatives = getRecord(import_id,relative_id)['relatives']
                otherCitizenDataRelatives.remove(citizen_id)
                changeRecord(import_id,relative_id,{'relatives': otherCitizenDataRelatives})

    return changeRecord(import_id,int(citizen_id),{'relatives':new_relatives})