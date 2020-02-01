from m_finger.models import *
from django.db.models import Q
import time
"""
def RunAccess(value):
    list = Rfid.objects.filter(rfid = value)
    quantity = list.count()
    if quantity > 0:
        return True
    else:
        return False





def RunActiv(value):
    bool = Rfid.objects.get(id = value)

    if bool.activ:
        bool.activ = False
    else:
        bool.activ = True
    bool.save()






def RunShowVar(var):        # Показать переменную из базы
    status = Var_rfid.objects.filter(name = var)
    quantity = status.count()
    if quantity == 0:
        add = Var_rfid()
        add.name = var
        add.value = "NEW"
        add.save()
        return "NEW"
    else:
        status = Var_rfid.objects.get(name = var)
        return status.value


def RunDeleteRfid(value):
    rfid = Rfid.objects.get(id = value)
    rfid.delete()


def RunCheckRfid(value):   # Проверить есть ли в базе данных эта RFID метка
        list = Rfid.objects.filter(rfid = value)
        quantity = list.count()
        if quantity == 0:
            return True
        else:
            print = RunPrint("Метка", value, list)
            RunChangeVar("PRINT", print)
            return False
"""






def RunCheckFinger(value):
    list = Finger.objects.filter(number = value)
    quantity = list.count()
    if quantity == 0:
        return False
    else:
        RunChangeVar("STATUS", "NO")
        RunChangeVar("STEP", "NO")
        RunChangeVar("PRINT", RunPrint("Номер", value, list))
        return True
# Принт
def RunPrint(name, value, list):
    text = '<div style=\\"color:red\\">' + name + ': <br/>' + str(value) + "<br/>Принадлежит:"
    for uid in list:
         text = text + "<br/>" + uid.user.username + " " + uid.user.first_name
    text = text + "</div>"
    return text

#Ищет свободный идентификатор для отпечатка
def RunFree():
    fin = Finger.objects.all()
    for place in range(6):
        if not(any(place == id.number for id in fin)):
            return place
    return "FULL"

def RunCheckVar(var, value):        # Проверить переменную в базе
    status = Var_finger.objects.filter(name = var)
    quantity = status.count()
    if quantity == 0:
        add = Var_finger()
        add.name = var
        add.value = "NEW"
        add.save()
        return False
    else:
        status = Var_finger.objects.get(name = var)
        if status.value == value:
            return True
        else:
            return False


def RunChangeVar(var, value):       # Изменить переменную в базе
    if var == "USER":
        status = Var_finger.objects.filter(name = var)
        user = User.objects.get(id = value)
        quantity = status.count()
        if quantity == 0:
            add = Var_finger()
            add.name = var
            add.user = user
            add.save()
        else:
            status = Var_finger.objects.get(name = var)
            status.user = user
            status.save()
    else:
        status = Var_finger.objects.filter(name = var)
        quantity = status.count()
        if quantity == 0:
            add = Var_finger()
            add.name = var
            add.value = value
            add.save()
        else:
            status = Var_finger.objects.get(name = var)
            status.value = value
            status.save()


def RunSaveFinger(value):    # Сохранить Finger метку
        add = Finger()
        add.finger = value
        add.number = value
        add.contact = run.user
        add.save()
        RunChangeVar("STATUS", "SAVE")
        RunChangeVar("STEP", "YES")
