## Проект "Хабр"
## Командная разработка по методологии Agile: SCRUM
## Сайт для обучения

### Базовая документация к проекту

Основные системные требования:

* Ubuntu 20.04 LTS
* Python 3.8
* PostgreSQL 12
* Django 3.1
* Зависимости (Python) из requirements.txt

### Установка необходимого ПО
#### обновляем информацию о репозиториях
```
apt update
```
#### Установка nginx, СУБД PostgreSQL, Git, virtualenv, gunicorn
nginx
```
apt install nginx
```
СУБД PostgreSQL
```
apt install postgresql postgresql-contrib
После установки проверяем статус СУБД, командой: service postgresql status
```
Git
```
apt install git-core
```
virtualenv
```
apt install python3-venv
```
gunicorn
```
apt install gunicorn
```
#### Настраиваем виртуальное окружение
При необходимости, для установки менеджера пакетов pip выполняем команду:
```
apt install python3-pip
```
Создаем и активируем виртуальное окружение:
```
mkdir /opt/venv
python3 -m venv /opt/venv/xabr_env
source /opt/venv/xabr_env/bin/activate
```
Создаем директории под логи:
```
mkdir /opt/venv/xabr_env/run/
mkdir /opt/venv/xabr_env/logs/
mkdir /opt/venv/xabr_env/logs/nginx/
```
Устанавливаем права:
```
chown -R hh /opt/venv/xabr_env
```
Клонируем репозиторий:
```
git clone git@github.com:Dmitrii2019/xabr.git /opt/venv/xabr_env/src
cd xabr_env/
```
Ставим зависимости:
```
pip3 install -r /opt/venv/xabr_env/src/xabr/requirements.txt
```
#### «PostgreSQL» Запускаем интерпретатор команд сервера:
```
sudo -u postgres psql
```
Создаем BD
```
CREATE DATABASE Xabr;
```
Создаем пользователя 
```
CREATE USER "USER_NAME" with NOSUPERUSER PASSWORD 'PASSWORD';
```
Вобовляем превелегии
```
GRANT ALL PRIVILEGES ON DATABASE Xabr TO "USER_NAME";
```
Выставляем кодировку 'UTF8'
```
ALTER ROLE "USER_NAME" SET CLIENT_ENCODING TO 'UTF8';
```
Устанавливается уровень изоляции
```
ALTER ROLE "USER_NAME" SET default_transaction_isolation TO 'READ COMMITTED';
```
Выставляем TIME ZONE
```
ALTER ROLE "USER_NAME" SET TIME ZONE "TIME ZONE";
```
Для выхода пишем «\q».
#### Суперпользователь
```
python3 manage.py createsuperuser
```
к примеру (логин/пароль): admin:admin
#### Выполнение миграций и сбор статических файлов проекта
Выполняем миграции:
```
python3 manage.py migrate
```
Собираем статику:
```
python3 manage.py collectstatic
```
#### Заполнить базу данных тестовыми данными (не обязательно)
```
python3 manage.py fill_db
```
#### Импортируем данные (не обязательно)
```
python manage.py loaddata db.json
```
#### Тест запуска
```
python3 manage.py runserver
```
#### Назначение прав доступа
```
chown -R xabr /home/xabr_env/
chmod -R 755 /home/xabr_env/xabr/
```
Настроим параметры службы «gunicorn»
```
sudo nano /etc/systemd/system/gunicorn.service


[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=USER_NAME
Group=www-data
WorkingDirectory=/home/xabr_env/xabr
ExecStart=/home/xabr_env/xabr/bin/gunicorn --access-logfile - --workers 3 --bind unix:/home/xabr_env/xabr/xabr.sock xabr.wsgi

[Install]
WantedBy=multi-user.target

```
Активирование и запуск сервиса
```
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
sudo systemctl status gunicorn
```
Настройки параметров для nginx
```
sudo nano /etc/nginx/sites-available/xabr.conf

server {
    listen 80;
    server_name 151.248.117.226; ### server_name необхоимо написать ip-адрес сервера

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/xabr_env/xabr;
    }

    location /media/ {
        root /home/xabr_env/xabr;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/xabr/xabr/xabr.sock;
    }
}
```
Перезапускаем службу «nginx»
```
sudo systemctl restart nginx
```
#### Активировируем сайт
```
sudo ln -s /etc/nginx/sites-available/xabr /etc/nginx/sites-enabled
```

### После этого в браузере можно ввести ip-адрес сервера и откроется проект.
#### Выкат изменений из Git:
```
source /opt/venv/xabr/bin/activate
cd /opt/venv/xabr/src
git pull origin master
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py collectstatic