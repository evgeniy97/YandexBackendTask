
# coding: utf-8

# In[1]:


import json


# In[2]:


def makeCitizen(citizen_id,town,birth_date="10.01.2000",relatives=[],
                street="No street",gender="male",name="Noname",building="1",apartament=1):
    return { 
        "citizen_id": citizen_id,
        "town": town,
        "birth_date": birth_date,
        "relatives": relatives,
        "street": street,
        "gender": gender,
        "name": name,
        "building": building,
        "apartament": apartament
            }


# In[3]:


def giveTown():
    for i in range (5001): yield "Moscow"
    for j in range(5001): yield "Kiev"
    yield "Berlin"    


# In[4]:


data = [makeCitizen(i,next(giveTown())) for i in range(2,10001)]


# In[5]:


next(giveTown())


# In[6]:


first_relatives = []
for i in range(1,10):
    data.append(makeCitizen(10000+i, next(giveTown()),birth_date="10.0{}.1990".format(i%10),relatives=[1]))
    first_relatives.append(10000+i)

data.append(makeCitizen(1,next(giveTown()),first_relatives))
for j in range(1, 10):
    data.append(makeCitizen(10010+j, next(giveTown()),birth_date="10.0{}.1990".format(i%10),relatives=[10010+j]))


# In[7]:

data = {"citizens": data}

with open('jsons/big_data.json', 'w') as f:
    json.dump(data, f,ensure_ascii=False)

