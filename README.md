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

| $ | sudo apt-get install mc python3 python3-dev apache2 libapache2-mod-wsgi-py3 python3-pip |
|---|:-------------|
| $ | sudo pip3 install django |

Права:

| $ | sudo chmod -R 777 /home |
|---|:-------------|

Зайдем в папку:

| $ | cd /home |
|---|:-------------|

Создадим проект:

| $ | django-admin.py startproject DomoPhone |
|---|:-------------|

Зайдем в папку проекта:

| $ | cd /home/DomoPhone |
|---|:-------------|

Сделаем миграцию:

| $ | python3 manage.py makemigrations |
|---|:-------------|
| $ | python3 manage.py migrate |

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
 DocumentRoot /home/DomoPhone
 WSGIScriptAlias / /home/DomoPhone/DomoPhone/wsgi.py

 # adjust the following line to match your Python path
 WSGIDaemonProcess mysite.example.com processes=2 threads=15 display-name=%{GROUP}
#python-home=/home/vhosts/mysite/venv/lib/python3.5
 WSGIProcessGroup mysite.example.com

 <directory /home/DomoPhone>
   AllowOverride all
   Require all granted
   Options FollowSymlinks
 </directory>

 Alias /static/ /home/DomoPhone/static/

 <Directory /home/DomoPhone/static>
  Require all granted
 </Directory>
</VirtualHost>
```

Активируем наш файл:

| $ | sudo systemctl reload apache2 |
|---|:-------------|
| $ | sudo a2ensite DomoPhone |
| $ | sudo apachectl restart |

## Установка Samba

| $ | sudo apt-get install samba samba-common-bin |
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

| $ | cd /home |
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
| $ | sudo chmod -R 777 /var/log |




## Настроить WSGI в проекте:
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

sys.path.append('/home/DomoPhone')
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
и там же внизу:

```python
STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
```

## Собрать статические файлы
Создать в проекте папку static и:

| $ | sudo python3 manage.py collectstatic |
|---|:-------------|

### Установка Celery

| $ | sudo pip3 install celery redis |
|---|:-------------|
| $ | sudo apt-get install redis-server |

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

Создать новый файл в своем приложении и добавить туда код tasks.py:
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

| $ | cd /var/www/DomoPhone |
|---|:-------------|
| $ | celery -A DomoPhone worker -B -l INFO |

### Установка Channels

| $ | pip3 install channels |
|---|:-------------|
| $ | pip3 install asgi_redis |

Добавим настройки:
```python
# Channels settings
CHANNEL_LAYERS = {
   "default": {
       "BACKEND": "asgi_redis.RedisChannelLayer",  # use redis backend
       "CONFIG": {
           "hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],  # set redis address
       },
       "ROUTING": "DomoPhone.routing.channel_routing",  # load routing from our routing.py file
   },
}
```
Создайте файл routing.py в дериктории настроек.

```python
from channels import route
from jobs import consumers

channel_routing = [
   # Wire up websocket channels to our consumers:
   route("websocket.connect", consumers.ws_connect),
   route("websocket.receive", consumers.ws_receive),
]
```

### Установка Mosquitto

| $ | sudo apt install mosquitto |
|---|:-------------|
| $ | sudo systemctl enable mosquitto.service |

Узнаем порт:

| $ | mosquitto -v |
|---|:-------------|

Узнаем IP:

| $ | hostname -I |
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

Открытие портов UART yf RPI4:

Заходим в меню sudo __raspi-config --> 5 --> P6__ Жмем NO потом YES

Заходим в файл __boot/config.txt__ и добавляем в раздел __[all]__
```python
dtoverlay=uart2
dtoverlay=uart3
dtoverlay=uart4
dtoverlay=uart5
```
Открыть только нужные интерфейсы
```python
GPIO14 = TXD0 -> ttyS0
GPIO15 = RXD0 -> ttyS0

Не использовать
GPIO0  = TXD2 -> ttyAMA1
GPIO1  = RXD2 -> ttyAMA1

GPIO4  = TXD3 -> ttyAMA2
GPIO5  = RXD3 -> ttyAMA2

GPIO8  = TXD4 -> ttyAMA3
GPIO9  = RXD4 -> ttyAMA3

GPIO12 = TXD5 -> ttyAMA4
GPIO13 = RXD5 -> ttyAMA4
```
и перезагружаем:

| $ | sudo reboot |
|---|:-------------|

## Библиотека для дисплея

установка:

| $ | sudo apt install python3-dev python3-pip libfreetype6-dev libjpeg-dev build-essential libopenjp2-7 libtiff5 |
|---|:-------------|
| $ | sudo -H pip3 install --upgrade luma.oled |
| $ | sudo usermod -a -G i2c,spi,gpio pi |
| $ | sudo apt install libsdl-dev libportmidi-dev libsdl-ttf2.0-dev libsdl-mixer1.2-dev libsdl-image1.2-dev |

 Клонируйте этот репозиторий:

| $ | git clone https://github.com/rm-hull/luma.examples.git |
|---|:-------------|
| $ | cd luma.examples |

Установите библиотеки luma, используя:

| $ | sudo -H pip3 install -e . |
|---|:-------------|

Запуск примеров:

| $ | cd luma.examples/examples |
|---|:-------------|
| $ | python3 3d_box.py --display ssd1309 --interface spi, -i spi |

[Подробнее](https://github.com/rm-hull/luma.examples)

[Библиотека](https://luma-oled.readthedocs.io/en/latest/intro.html)
## Пины:

__Дисплей:__

| Display      | --> | Raspberry PI4 |
|:------------:|:---:|:-------------:|

| PIN | --> | PIN | GPIO | SPI       |
|:---:|:---:|:---:|:----:|:---------:|
| CS  | --> | 24 | 8     | SPI0_CE0  |
| DC  | --> | 18 | 24    |           |
| RES | --> | 22 | 25    |           |
| SDA | --> | 19 | 9     | SPI0_MOSI |
| SCL | --> | 23 | 11    | SPI0_CLK  |
| VCC | --> | 1  |       | +3.3V     |
| GND | --> | 25 |       | GND       |

__Считыватель меток:__

| RFID         | --> | Raspberry PI4 |
|:------------:|:---:|:-------------:|

| PIN | --> | PIN | GPIO | SPI       |
|:---:|:---:|:---:|:----:|:---------:|
| TX  | --> | 10  | 15   | RXD0_UART |
| RX  | --> | 8   | 14   | TXD0_UART |
| VCC | --> | 4   |      | +5.0V     |
| GND | --> | 6   |      | GND       |

__Датчик отпечатков пальца:__

| Finger       | --> | Raspberry PI4 |
|:------------:|:---:|:-------------:|

| PIN |      COLOR      | --> | PIN | GPIO | SPI       |
|:---:|:---------------:|:---:|:---:|:----:|:---------:|
| TX  |      BLUE       | --> | 33  | 13   | RXD5_UART |
| RX  |      GREEN      | --> | 32  | 12   | TXD5_UART |
| VCC | BLACK and WHITE | --> | 1   |      | +3.3V     |
| GND |     YELLOW      | --> | 34   |      | GND       |

## Полезные ссылки:

[Установка Celery c Django](http://docs.celeryproject.org/en/latest/django/first-steps-with-django.html)
