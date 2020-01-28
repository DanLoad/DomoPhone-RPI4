# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
import time
from celery.schedules import timedelta
from celery.task import task, periodic_task


from celery.schedules import crontab
#@periodic_task(run_every=(crontab(minute='*****')),name="test")

#@periodic_task(ignore_result=True, run_every=5)
@shared_task(ignore_result=True, max_retries=1, default_retry_delay=10)
def test():
    print(">>>>>>>>>>>>>>>")
    time.sleep(7)
    print("<<<<<<<<<<<<")

@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)
