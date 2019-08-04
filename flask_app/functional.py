from datetime import datetime, date
import numpy as np
from dataBaseTools import dbLen, addRecords2DB, getAllRecords, changeRecord, getRecord

def minMax(a,b):
    return (min(a,b), max(a,b))


class Relatives(object):
    """
    The structure required to verify family ties
    """
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
    Receives a list of lives on entry, looks at the correctness
    family ties. We go through all the inhabitants and add a couple
    (my_id, my_relatives_id) to the unclosed_id list if there is no such pair in the list.
    If there is such a pair, then remove it from the list. If my_id == my_relatives_id,
    don't do anything
    """
    unclosed_id = Relatives()
    for person in data:
        for relative_id in person["relatives"]:
            unclosed_id.add(person['citizen_id'], relative_id)
    return unclosed_id.is_opened() == False

def calculateAge(birthDate):
    """
    Returns int: age of resident
    """
    date_of_birth = datetime.strptime(birthDate, "%d.%m.%Y")
    today = date.today()
    return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))


def getCitizen(import_id, citizen_id):
    """
    Returns a record from the database
    """
    return getRecord(import_id,int(citizen_id))

def getCitizenMonth(import_id, citizen_id):
    """
    Returns str: month of birth in MM format (1 - for January, etc. ..)
    """
    return str(int(getCitizen(import_id, citizen_id)['birth_date'][3:5])) # str(int('01')) -> '1'

def calculatePresents(import_id):
    """
    Calculates the number of gifts a resident buys in each month
    """
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
        
        for month, number in relativesMonth.items():
            returnedMonth[month].append(
                {
                    "citizen_id": person['citizen_id'],
                    "presents": number
                }
            )

    return returnedMonth

def calculatePercentile(city_name, ages):
    """
    Calculates percentiles in the given format
    """
    return {
        "town": city_name,
        "p50": np.percentile(ages,50,interpolation='linear'),
        "p75": np.percentile(ages,75,interpolation='linear'),
        "p99": np.percentile(ages,99,interpolation='linear')
    }

def calculatePercentileFunctional(import_id):
    """
    The function calculates the percentiles - to begin with, it is from the specified import
    calculates all ages and scatters them by city, then a couple
    the city and the age of the city residents passes calculatePercentile
    """
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
    """
    The function changes the record in the database
    """
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

        for relative_id in new_relatives:
            if not relative_id in old_relatives:
                """
                1) Get the data of this resident, take from him his relatives
                2) Add the current resident to the list
                3) Update the list of relatives
                """
                otherCitizenDataRelatives = getRecord(import_id,relative_id)['relatives']
                otherCitizenDataRelatives.append(citizen_id)
                changeRecord(import_id,relative_id,{'relatives': otherCitizenDataRelatives})
        
        for relative_id in old_relatives:
            if not relative_id in new_relatives:
                """
                1) Get the data of this resident, take from him his relatives
                2) Delete the current resident in the list
                3) Update the list of relatives
                """
                otherCitizenDataRelatives = getRecord(import_id,relative_id)['relatives']
                otherCitizenDataRelatives.remove(citizen_id)
                changeRecord(import_id,relative_id,{'relatives': otherCitizenDataRelatives})

    return changeRecord(import_id,int(citizen_id),{'relatives':new_relatives})