## Проект "Хабр"
## Командная разработка по методологии Agile: SCRUM
## Сайт для обучения

### Базовая документация к проекту

Основные системные требования:

* archlinux-2022.08.05
* python-3.10.6-1-x86_64
* nginx-1.22.0-2-x86_64
* postgresql-14.5-1-x86_64
* django 3.2.14
* gunicorn 20.1.0
* Зависимости (python) из requirement.txt

### Установка необходимого ПО
Обновляем информацию о репозиториях
```
pacman -Suy
```
#### Установка nginx, postgresql, git, python, python-pip
```
pacman -S nginx postgresql git python python-pip
```
#### Настраиваем виртуальное окружение
Создаем и активируем виртуальное окружение
```
mkdir /srv/http/Habr && cd /srv/http/Habr
python3 -m venv venv
source venv/bin/activate
```
На https://github.com/settings/keys добавляем наш ключ
```
cat ~/.ssh/id_rsa.pub ---> https://github.com/settings/keys
```
Клонируем репозиторий:
```
git clone git@github.com:uRufus/Habr.git
cd Habr/ && mv * .. && cd .. && rm -rf Habr/
```
Ставим зависимости:
```
python3 venv/bin/pip3 install -r requirement.txt
```
#### Postgresql. Запускаем интерпретатор команд сервера:
```
sudo -iu postgres
[postgres]$ initdb --locale=ru_RU.UTF-8 -E UTF8 -D /var/lib/postgres/data
exit
systemctl enable postgresql.service && systemctl start postgresql.service
```
Добавляем пользователя
```
useradd -m habr -G wheel
```
Создаем БД
```
sudo -iu postgres
[postgres@arch ~]$ createuser --interactive
Введите имя новой роли: habr
Должна ли новая роль иметь полномочия суперпользователя? (y - да/n - нет) n
Новая роль должна иметь право создавать базы данных? (y - да/n - нет) n
Новая роль должна иметь право создавать другие роли? (y - да/n - нет) n
[postgres@arch ~]$ createdb habr
exit
```
Перезапускам Postgresql
```
systemctl restart postgresql
```
Проверяем доступность postgresql базы проекте
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'habr',
        'USER': 'habr',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': 5432,
    }
}
```
#### Назначение прав доступа
```
cd /srv/http/Habr/
chown -R habr:habr *
find . -type d -exec chmod 755 {} \;
find . -type f -exec chmod 644 {} \;
```
#### Выполнение миграций проекта
Работаем о пользователя habr
```
sudo -iu habr
```
Выполняем миграции
```
cd /srv/http/Habr/myHabr
../venv/bin/python3 manage.py makemigrations
../venv/bin/python3 manage.py migrate
../venv/bin/python3 manage.py fill_db
```
#### Тест запуска
```
../venv/bin/python3 manage.py runserver 0.0.0.0:8000
Ctrl-C
exit
```
#### Установка gunicorn.
Настроим параметры службы «gunicorn» - gunicorn.sock
```
../venv/bin/python3 /srv/http/Habr/venv/bin/pip3 install gunicorn psycopg2-binary 
```
```
vim /etc/systemd/system/gunicorn.socket
```
```
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.socket
SocketUser=http

[Install]
WantedBy=sockets.target
```
и
```
vim /etc/systemd/system/gunicorn.service
```
```
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=habr
Group=habr
WorkingDirectory=/srv/http/Habr/myHabr
ExecStart=/srv/http/Habr/venv/bin/gunicorn --access-logfile - --workers 5 --bind unix:/run/gunicorn.socket myHabr.wsgi:application

[Install]
WantedBy=multi-user.target
```
Активирование и запуск сервиса
```
systemctl daemon-reload
systemctl enable gunicorn.socket
systemctl start gunicorn.socket
systemctl enable gunicorn
systemctl start gunicorn
systemctl status gunicorn
```
#### Настройка nginx
Содержимое /etc/nginx/nginx.conf
```
user http;
worker_processes 2;
worker_cpu_affinity auto;

events {
    multi_accept on;
    worker_connections 16;
}

http {
    charset utf-8;
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    server_tokens off;
    log_not_found off;
    types_hash_max_size 4096;
    client_max_body_size 16M;

    include mime.types;
    default_type application/octet-stream;

    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log warn;

    upstream app_servers2 {
        server unix:/run/gunicorn.socket fail_timeout=0;
    }

    include /etc/nginx/sites-enabled/*;
}
```
Создаем два каталога: /etc/nginx/sites-available и /etc/nginx/sites-enabled 
```
mkdir /etc/nginx/sites-available
mkdir /etc/nginx/sites-enabled
```
```
vim /etc/nginx/sites-available/kibarium.ru
```
```
server {
  server_name kibarium.ru www.kibarium.ru;
  access_log /var/log/nginx/kibarium.ru.access.log;
  error_log /var/log/nginx/kibarium.ru.error.log;


  location /static/ {
    alias /srv/http/Habr/myHabr/static/;
  }

  location /media/ {
    alias /srv/http/Habr/myHabr/media/;
  }

  location /images/ {
    alias /srv/http/Habr/myHabr/static/images/;
  }

  location / {
    proxy_pass         http://app_servers2;
    proxy_redirect     off;
    proxy_set_header   Host $host;
    proxy_set_header   X-Real-IP $remote_addr;
    proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header   X-Forwarded-Host $server_name;

    auth_basic "Restricted Access!";
    auth_basic_user_file /srv/http/Habr/.htpasswd;
  }


  listen 443 ssl; # managed by Certbot
  ssl_certificate /etc/letsencrypt/live/kibarium.ru/fullchain.pem; # managed by Certbot
  ssl_certificate_key /etc/letsencrypt/live/kibarium.ru/privkey.pem; # managed by Certbot
  include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
  ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem; # managed by Certbot

}

server {
  if ($host = kibarium.ru) {
      return 301 https://$host$request_uri;
  } # managed by Certbot

  listen 80;
  server_name kibarium.ru www.kibarium.ru;
    return 404; # managed by Certbot
}
```
#### Активируем сайт
```
ln -s /etc/nginx/sites-available/kibarium.ru /etc/nginx/sites-enabled/kibarium.ru
```
Включаем в загрузку
```
systemctl enable nginx.service
```
Перезапускаем службу nginx
```
systemctl restart nginx.service
```
Теперь можно перезапустить сервер
```shell
shutdown -r now
```
### После этого в браузере по адресу https://kibarium.ru открывается проект.