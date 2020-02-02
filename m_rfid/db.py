from m_rfid import my_settings
from m_rfid.models import *
from django.db.models import Q
import time

def RfidAccess(value):
    list = Rfid.objects.filter(rfid = value)
    quantity = list.count()
    if quantity > 0:
        return True
    else:
        return False


def RfidSave(value):        ## Сохранить RFID метку
    run = Var_rfid.objects.get(name = "USER")
    add = Rfid()
    add.rfid = value
    add.user = run.user
    add.save()
    return True


def RfidCheck(value):   ## Проверить есть ли в базе данных эта RFID метка
        list = Rfid.objects.filter(rfid = value)
        quantity = list.count()
        if quantity == 0:
            return True
        else:
            print = RunPrint("Метка", value, list)
            RunChangeVar("PRINT", print)
            return False




def RfidPrint(name, value, list):
    text = '<div style=\\"color:red\\">' + name + ': <br/>' + str(value) + "<br/>Принадлежит:"
    for uid in list:
         text = text + "<br/>" + uid.user.username + " " + uid.user.first_name
    text = text + "</div>"
    return text


def RfidActiv(value):
    bool = Rfid.objects.get(id = value)

    if bool.activ:
        bool.activ = False
    else:
        bool.activ = True
    bool.save()


def RfidChangeVar(var, value):       # Изменить переменную в базе
    if var == "USER":
        status = Var_rfid.objects.filter(name = var)
        user = User.objects.get(id = value)
        quantity = status.count()
        if quantity == 0:
            add = Var_rfid()
            add.name = var
            add.user = user
            add.save()
        else:
            status = Var_rfid.objects.get(name = var)
            status.user = user
            status.save()
    else:
        status = Var_rfid.objects.filter(name = var)
        quantity = status.count()
        if quantity == 0:
            add = Var_rfid()
            add.name = var
            add.value = value
            add.save()
        else:
            status = Var_rfid.objects.get(name = var)
            status.value = value
            status.save()


def RfidCheckVar(var, value):        ## Проверить переменную в базе
    status = Var_rfid.objects.filter(name = var)
    quantity = status.count()
    if quantity == 0:
        add = Var_rfid()
        add.name = var
        add.value = "NEW"
        add.save()
        return False
    else:
        status = Var_rfid.objects.get(name = var)
        if status.value == value:
            return True
        else:
            return False


def RfidShowVar(var):        # Показать переменную из базы
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


def RfidDelete(value):
    rfid = Rfid.objects.get(id = value)
    rfid.delete()
