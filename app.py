import os 
from flask import Flask, request, jsonify, Response

from dataBaseTools import dbLen, addRecords2DB, getAllRecords

app = Flask(__name__)


@app.route('/')
def hello():
    return "Hello, this is implication of yandex backend school's task by Evgeniy Khomutov"


@app.route('/imports',methods=['POST'])
def post():
    if request.method == 'POST':
    # проверяем, что прислали файл НАДО ПРОВЕРИТЬ ЧТО ЭТО JSON
        if 'file' not in request.files:
            return "someting went wrong 1"
    
    ### MagicCode 
    ### Проверить данные 
    ### Получить import_id
    import_id = dbLen + 1
    ### Положить в БД

    # Если успешно, то присылаем код 201 и json файл - Как присылать HTTP статус?

    return Response(jsonify(
        {
            "data":
            {
                "import_id": import_id
            }
        }
    ), status=201)

@app.route('/PATCH')
def patch():
    pass

@app.route('/GET')
def get():
    pass

@app.route('/test_<name>')
def FUNCTION(name):
    return(name)

if __name__ == '__main__':
    app.run()