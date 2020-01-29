from m_rfid import my_settings
from m_rfid.models import *
from django.db.models import Q
import time

def RunAccess(value):
    list = Rfid.objects.filter(rfid = value)
    quantity = list.count()
    if quantity > 0:
        return True
    else:
        return False


def RunSave(value):
    add = Rfid()
    add.rfid = value
    add.contact = run.user
    add.save()


def RunCheckValue(value):
        list = Rfid.objects.filter(rfid = value)
        quantity = list.count()
        if quantity == 0:
            return True
        else:
            settings.RFID_PRINT = RunPrint("Метка", value, list)
            settings.configure(RFID_STATUS="PRINT")
            return False

def RunPrint(name, value, list):
    text = '<div style=\\"color:red\\">' + name + ': <br/>' + str(value) + "<br/>Принадлежит:"
    for uid in list:
         text = text + "<br/>" + uid.contact.name + " " + uid.contact.firstname
    text = text + "</div>"
    return text


def RunActiv(value):
    bool = Rfid.objects.get(id = value)

    if bool.activ:
        bool.activ = False
    else:
        bool.activ = True
    bool.save()


def RunStart():
    settings.configure(RFID_STATUS="REC")
    #run = Status.objects.get(comand = "run")
    #user = User.objects.get(id = iuser)
    #run.module = module
    #run.user = user
    #run.time = time.time() + timeOver
    #run.status = status
    #run.step = step
    #run.number = " "
    #if not(status == "up" or status == "down"):
    #    run.up = 0
    #    run.down = 0
    #run.print = " "
    #run.save()

def RunStop():
    settings.configure(RFID_STATUS="STOP")
    #run = Status.objects.get(comand = "run")
    #run.status = "stop"
    #run.save()
