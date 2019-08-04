
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
        "apartment": apartament
            }


# In[3]:


def giveTown():
    for i in range (5000): yield "Moscow"
    for j in range(5000): yield "Kiev"
    for k in range(18): yield "Berlin"    


# In[4]:


data = [makeCitizen(i,next(giveTown())) for i in range(2,10001)]


# In[5]:


next(giveTown())


# In[6]:


first_relatives = []
for i in range(1,10):
    data.append(makeCitizen(10000+i, "NOPE",birth_date="10.0{}.1990".format(i%9 + 1),relatives=[1]))
    first_relatives.append(10000+i)

data.append(makeCitizen(1,"NOPE",relatives=first_relatives))
for j in range(1, 10):
    data.append(makeCitizen(10010+j, "NOPE",birth_date="10.0{}.1990".format(j%9 + 1),relatives=[10010+j]))


# In[7]:


gen = giveTown()
for i, town in enumerate(gen):
    data[i]['town'] = town


# In[8]:


data = {"citizens": data}


# In[9]:


with open('jsons/big_data.json', 'w') as f:
    json.dump(data, f)

