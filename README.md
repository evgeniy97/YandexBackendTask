# YandexBackendTask
## Описание

Для реализации задания используется связка из GUNICORN+Flask и MongoBD

## Инструкция
### Развертывание

### Последоватеность команд для консоли (простая установка на Ubuntu без Unicorn и Docker) :  
sudo apt install git  
git clone https://github.com/evgeniy97/YandexBackendTask.git  
sudo apt install python3-pip  
pip3 install 'numpy==1.14.6'  'flask==0.12.2'  'marshmallow==3.0.0rc8' 'pymongo==3.8.0' 'requests==2.18.4'  
 * Follow mongodb install instruction https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/ *  
sudo mkdir -p /data/db  
sudo chown -R `id -un` /data/db  

### Последоватеность команд для консоли:  
 * Follow docker install instruction https://www.digitalocean.com/community/tutorials/docker-ubuntu-18-04-1-ru*  
 * Устанавливаем контейнер mongodb *  

sudo docker system prune -a
sudo docker run -d -p 127.0.0.1:27017:27017 --restart always --name mongoDB mongo   
git clone https://github.com/evgeniy97/YandexBackendTask.git  
cd YandexBackendTask  
cd flask_app  
sudo docker build --tag flask_gunicorn_app .  
sudo docker run --detach -p 80:8000 --restart always flask_gunicorn_app   
sudo docker container ls -a

### To run tests  
cd YandexBackendTask  
cd test  
python3 autotest.py

В качестве ответа должно получиться коды ответа запросов от сервера  



## TO Do
- Разобраться с NGINX и нужен ли он здесь? [link](https://medium.com/@kmmanoj/deploying-a-scalable-flask-app-using-gunicorn-and-nginx-in-docker-part-2-fb33ec234113)  
- Разобраться с blueprint, возможно использовать их в проекте  
- Как протестировать на серваке?  
- Как протестировать работу с одновременными запросами?  



### Тестирование
Для простого тестирования достаточно запустить БД, сервер и файл autotest.py из папки test. Важно, что-бы все json файлы лежали в папке jsons. Тестирование предназначенно для тестирования функционала сервера и не тестирует NGINX и GUNICORN, поэтому запускается отдельно от них и не в контейнере.