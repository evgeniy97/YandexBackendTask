from datetime import datetime, date
import numpy as np

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

def calculatePresents(data):
    return []

def calculatePercentile(city_name, ages):
    return {
        "town": city_name,
        "p50": np.percentile(ages,50,interpolation='linear'),
        "p75": np.percentile(ages,75,interpolation='linear'),
        "p99": np.percentile(ages,99,interpolation='linear')
    }