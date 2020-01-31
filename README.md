# DomoPhone на Raspberry PI 4

## Установка статического IP

Заходим в файл конфигурации:

| $ | sudo nano /etc/dhcpcd.conf |
|---|-------------:|

В конце файла дописываем следующую строчку, чтобы игнорировать DHCP сервера, и назначить нужные нам настройки:
```
nodhcp
```
После этой строки назначим статический адрес для проводного подключения:
```
interface eth0
static ip_address=192.168.1.101/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1

interface wlan0
static ip_address=192.168.1.101/24
static routers=192.168.1.1
static domain_name_servers=192.168.1.1
```

И перезагрузить:

| $ | sudo reboot |
|---|-------------:|

## Установка Django Apach2 wsgi:
Обновляем систему:

| $ | sudo apt-get update |
|---|:-------------|
| $ | sudo apt-get upgrade |

Устанавливает pip, Apach2, mod wsgi:

| $ | sudo apt-get install mc python3 python3-dev apache2 libapache2-mod-wsgi-py3 python3-pip samba samba-common-bin |
|---|:-------------|
| $ | sudo pip3 install django |

Откроем файл:

| $ | sudo nano /etc/apache2/apache2.conf |
|---|:-------------|

И вставим в конце:
```python
ServerName localhost
```

Исправим корневую папку на с /var/www/html на /var/www

| $ | sudo nano /etc/apache2/sites-available/000-default.conf |
|---|:-------------|

Создать файл конфигурации Apach2 с именем проекта:

| $ | sudo nano /etc/apache2/sites-available/DomoPhone.conf |
|---|:-------------|

Вставить и изменить на свои пути:
```python
<VirtualHost *:80>
 ServerName 192.168.1.101
 DocumentRoot /var/www/DomoPhone
 WSGIScriptAlias / /var/www/DomoPhone/DomoPhone/wsgi.py

 # adjust the following line to match your Python path
 WSGIDaemonProcess mysite.example.com processes=2 threads=15 display-name=%{GROUP}
#python-home=/var/www/vhosts/mysite/venv/lib/python3.5
 WSGIProcessGroup mysite.example.com

 <directory /var/www/DomoPhone>
   AllowOverride all
   Require all granted
   Options FollowSymlinks
 </directory>

 Alias /static/ /var/www/DomoPhone/static/

 <Directory /var/www/DomoPhone/static>
  Require all granted
 </Directory>
</VirtualHost>
```

Активируем наш файл:

| $ | sudo systemctl reload apache2 |
|---|:-------------|
| $ | sudo a2ensite DomoPhone |
| $ | sudo apachectl restart |

Заходим в директорию в которой хотим создать проект:

| $ | cd /var/www |
|---|:-------------|

Создаем проект:

| $ | django-admin startproject DomoPhone |
|---|:-------------|

Теперь настроим Samba. Для этого открываем файл конфигурации:

| $ | sudo nano /etc/samba/smb.conf |
|---|:-------------|

И добавляем в конец файла следующие настройки:
```python
[DomoPhone]
Comment = DomoPhone folder
Path = /
Browseable = yes
Writeable = yes
only guest = no
create mask = 0777
directory mask = 0777
Public = yes
Guest ok = yes
```

Открываем доступ папкам:

| $ | cd /var/www |
|---|:-------------|
| $ | chmod 664 ./DomoPhone/db.sqlite3 |
| $ | chmod 775 ./DomoPhone |

Теперь надо дать группе www-data права:

| $ | sudo chown :www-data ./DomoPhone/db.sqlite3 |
|---|:-------------|
| $ | sudo chown :www-data ./DomoPhone |

Папкам:

| $ | sudo chmod -R 777 /home |
|---|:-------------|
| $ | sudo chmod -R 777 /var/www/log |




Настроим наш проект:
В wsgi.py вставить:


```python
"""
WSGI config for DomoPhone project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
import time
import traceback
import signal
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/DomoPhone')
# adjust the Python version in the line below as needed
#sys.path.append('/usr/lib/python3.5/site-packages')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DomoPhone.settings')

try:
    application = get_wsgi_application()
except Exception:
    # Error loading applications
    if 'mod_wsgi' in sys.modules:
        traceback.print_exc()
        os.kill(os.getpid(), signal.SIGINT)
        time.sleep(2.5)
```

В проекте Django в файле настроек settings.py вписать:
```python
ALLOWED_HOSTS = ["192.168.1.101", "127.0.0.1", "127.0.1.1"]
```

### Установка Celery

| $ | sudo pip3 install Celery redis |
|---|:-------------|

Откройте файл настроек settings.py в вашем проекте Django
Добавим связанные с Celery/Redis конфиги:
```python
# celery
CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
```

Потом нужно создать новый файл и добавить туда код
file: DomoPhone/DomoPhone/celery.py
```python
from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DomoPhone.settings')

app = Celery('DomoPhone')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
```

Добавить код в файл в той же дериктории:
```python
# proj/proj/__init__.py:
from __future__ import absolute_import, unicode_literals

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)
```

Создать новый файл и добавить туда код DomoPhone/tasks.py:
```python
# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
```

Для проверки работы Celery:

| $ | celery -A DomoPhone worker -B -l INFO |
|---|:-------------|

## Установка библиотек:

Библиотека для UART

| $ | sudo pip3 install pyserial |
|---|:-------------|

Библиотека для Датчика отпечатка пальца

| $ | sudo apt-get install python-fingerprint |
|---|:-------------|

Библиотека для создания программ в Django

| $ | sudo pip3 install django-crontab |
|---|:-------------|

Библиотека RF

| $ | sudo pip3 install rpi-rf |
|---|:-------------|

Библиотека Raspberry GPIO

| $ | sudo pip3 install RPi.GPIO |
|---|:-------------|

## Полезные ссылки:

[Установка Celery c Django](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
