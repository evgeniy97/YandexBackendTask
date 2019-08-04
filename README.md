# YandexBackendTask
## Описание

Для реализации задания используется связка из NGINX+GUNICORN+Flask и MongoBD

## Инструкция
### Развертывание

gdffsdfentrant
6d8b422af8cec3ab6bb838ca114b9350ca318eaac55411b3968233482d92d178

### Последоватеность команд для консоли (простая установка на Ubuntu буз NGINX и Unicorn) : 
sudo apt install git
git clone https://github.com/evgeniy97/YandexBackendTask.git
sudo apt install python3-pip
pip3 install 'numpy==1.14.6'  'flask==0.12.2'  'marshmallow==3.0.0rc8' 'pymongo==3.8.0' 'requests==2.18.4'
 * Follow mongodb instruction https://docs.mongodb.com/manual/tutorial/install-mongodb-on-ubuntu/ * 
sudo mkdir -p /data/db
sudo chown -R `id -un` /data/db



### Тестирование
Для простого тестирования достаточно запустить БД, сервер и файл autotest.py из папки test. Важно, что-бы все json файлы лежали в папке jsons. Тестирование предназначенно для тестирования функционала сервера и не тестирует NGINX и GUNICORN, поэтому запускается отдельно от них и не в контейнере.