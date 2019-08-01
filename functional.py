
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

def calculateAge(person):
    return 42

def calculatePresents(data):
    return []

def calculatePercentile(data):
    pass