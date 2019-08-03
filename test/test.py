import requests

ADRESS = 'http://127.0.0.1:5000/'



response = requests.get(ADRESS)
print(response.status_code)


data = {'citizens': [{
    'citizen_id': 10,
    'town': 'Moscow',
    'street': 'Tverskaya',
    'building': '1c4',
    'apartment': 5,
    'name': 'Ivan',
    'birth_day': '10.04.2000',
    'gender': 'male'
    , 'relatives': []
},
    {
    'citizen_id': 12,
    'town': 'Moscow',
    'street': 'Tverskaya',
    'building': '1c4',
    'apartment': 5,
    'name': 'Ivan',
    'birth_day': '10.04.2000',
    'gender': 'male'
    , 'relatives': []
    }
] }

response = requests.post('http://127.0.0.1:5000/imports',json=data)
print(response.status_code, response.content)

response = requests.get("http://127.0.0.1:5000/imports/{}/citizens".format(1))
print(response.status_code, response.content)