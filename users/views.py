from django.shortcuts import render
from django.http import HttpResponse
from users.models import *
from own.models import *
from users.settings import *
from settings.models import *
#from users.templates.users.run_db import *
import json
from m_rfid.db import *
from m_finger.db import *
from m_rfid.models import *
from m_finger.models import *



def index(request):
    if not request.GET:
        user = User.objects.filter()
        rfid = Rfid.objects.filter()
        rf = RF.objects.filter()
        finger = Finger.objects.filter()
        return render(request, 'users/users.html', locals())


def change_user(request, user_id="0"):
    if not request.GET:
        user = User.objects.get(id = user_id)
        rfid = Rfid.objects.filter(user = user_id)
        #rf = RF.objects.filter(user = _id)
        finger = Finger.objects.filter(user = user_id)
        return render(request, 'users/includes/change_user.html', locals())


def add_finger(request):
    if request.GET and "user" == request.GET["cmd"]:
        user_id = request.GET["user"]
        user = User.objects.get(id = user_id)
        rfid = Rfid.objects.filter(user = user_id)
        #rf = RF.objects.filter(user = _id)
        finger = Finger.objects.filter(user = user_id)
        return render(request, 'm_finger/add_finger.html', locals())

def user_activ(request):
    if request.GET and "user" == request.GET["cmd"]:
        user_id = request.GET["user"]
        user = User.objects.get(id = user_id)
        rfid = Rfid.objects.filter(user = user_id)
        #rf = RF.objects.filter(user = _id)
        finger = Finger.objects.filter(user = user_id)
        return render(request, 'users/includes/user_activ.html', locals())



def user_owned(request):
    if request.GET and "user" == request.GET["cmd"]:
        user_id = request.GET["user"]
        user = User.objects.get(id = user_id)
        rfid = Rfid.objects.filter(user = user_id)
        #rf = RF.objects.filter(user = _id)
        finger = Finger.objects.filter(user = user_id)
        return render(request, 'users/includes/own_user.html', locals())
    else:
        pass



def all_owned(request):
    if request.GET and "all" == request.GET["cmd"]:
        user = User.objects.filter()
        rfid = Rfid.objects.filter()
        rf = RF.objects.filter()
        finger = Finger.objects.filter()

        return render(request, 'users/includes/info_all.html', locals())
    else:
        pass


def all_name(request):
    if request.GET and "all" == request.GET["cmd"]:
        user = User.objects.filter()
        rfid = Rfid.objects.filter()
        rf = RF.objects.filter()
        finger = Finger.objects.filter()
        return render(request, 'users/includes/info_user.html', locals())
    else:
        pass



def Run_rfid(request):

    if request.GET and "start" == request.GET["cmd"]:
        user_id = request.GET["user"]
        user_id = user_id[5:]
        RfidChangeVar("STATUS", "REC")
        RfidChangeVar("USER", user_id)
        return HttpResponse("Поднесите RFID метку к считывателю")



    elif request.GET and "stop" == request.GET["cmd"]:
        RfidChangeVar("STATUS", "STOP")
        return HttpResponse("Отменено")



    elif request.GET and "delete" == request.GET["cmd"]:
        user_id = request.GET["user"]
        index = request.GET["index"]
        user = User.objects.get(id = user_id)
        rfid = Rfid.objects.filter(user = user_id)
        #rf = RF.objects.filter(contact = user_id)
        finger = Finger.objects.filter(contact = user_id)
        RfidDelete(index)
        return render(request, 'users/includes/own_user.html', locals())



    elif request.GET and "activ" == request.GET["cmd"]:
        user_id = request.GET["user"]
        index = request.GET["index"]
        RfidActiv(index)
        user = User.objects.get(id = user_id)
        rfid = Rfid.objects.filter(user = user_id)
        #rf = RF.objects.filter(user = _id)
        finger = Finger.objects.filter(user = user_id)
        return render(request, 'users/includes/user_activ.html', locals())



    elif request.GET and "check" == request.GET["cmd"]:
        status = RfidShowVar("STATUS")
        if status == "REC":
            return HttpResponse('{"cmd": "REC"}')
        elif status == "NO":
            return HttpResponse('{"cmd": "NOT", "data": "' + RfidShowVar("PRINT") + '"}')
        elif status == "TIME":
            return HttpResponse('{"cmd": "TIME"}')
        elif status == "SAVE":
            return HttpResponse('{"cmd": "SAVE"}')
        else:
            return HttpResponse('{"cmd": "XXX"}')



def Run_rf(request):

    if request.GET and "open" == request.GET["cmd"]:
        user_id = request.GET["user"]
        user_id = user_id[5:]
        RunStart(user_id, "rf", "open", "no")
        return HttpResponse("ok")



    elif request.GET and "stop" == request.GET["cmd"]:
        RunStop()
        return HttpResponse("Отменено")



    elif request.GET and "delete" == request.GET["cmd"]:
        user_id = request.GET["user"]
        index = request.GET["index"]
        RunDelete("rf", index)
        contact = Contact.objects.get(id = user_id)
        rfid = Rfid.objects.filter(contact = user_id)
        rf = RF.objects.filter(contact = user_id)
        finger = Finger.objects.filter(contact = user_id)
        return render(request, 'users/includes/own_user.html', locals())



    elif request.GET and "up" == request.GET["cmd"]:
        user_id = request.GET["user"]
        user_id = user_id[5:]
        RunStart(user_id, "rf", "up", "no")
        return HttpResponse("Нажмите на кнопку брелка рядом с приемником")



    elif request.GET and "down" == request.GET["cmd"]:
        user_id = request.GET["user"]
        user_id = user_id[5:]
        RunStart(user_id, "rf", "down", "no")
        return HttpResponse("Нажмите на кнопку брелка рядом с приемником")



    elif request.GET and "save" == request.GET["cmd"]:
        if RunCheckValue("rf", " "):
            RunSave("rf", " ")
            return HttpResponse("Сохнанино")
        else:
            run = Status.objects.get(comand = "run")
            return HttpResponse(run.print)



    elif request.GET and "activ" == request.GET["cmd"]:
        user_id = request.GET["user"]
        index = request.GET["index"]
        RunActiv("rf", index)
        contact = Contact.objects.get(id = user_id)
        rfid = Rfid.objects.filter(contact = user_id)
        rf = RF.objects.filter(contact = user_id)
        finger = Finger.objects.filter(contact = user_id)
        return render(request, 'users/includes/own_user.html', locals())



    elif request.GET and "delete" == request.GET["cmd"]:
        user_id = request.GET["user"]
        index = request.GET["index"]
        contact = Contact.objects.get(id = user_id)
        rfid = Rfid.objects.filter(contact = user_id)
        rf = RF.objects.filter(contact = user_id)
        finger = Finger.objects.filter(contact = user_id)
        RunDelete("rf", index)
        return render(request, 'users/includes/own_user.html', locals())



    elif request.GET and "check" == request.GET["cmd"]:
        status = Status.objects.get(comand = "run")
        if status.status == "up":
            return HttpResponse('{"cmd": "up"}')
        elif status.status == "down":
            return HttpResponse('{"cmd": "down"}')
        elif status.status == "ok_up":
            return HttpResponse('{"cmd": "ok_up", "data": "' + RunReadId("rf", "up") + '"}')
        elif status.status == "ok_down":
            return HttpResponse('{"cmd": "ok_down", "data": "' + RunReadId("rf", "down") + '"}')
        elif status.status == "no":
            return HttpResponse('{"cmd": "no", "data": "' + RunRead() + '"}')
        elif status.status == "time":
            return HttpResponse('{"cmd": "time"}')
        elif status.status == "save":
            return HttpResponse('{"cmd": "save"}')
        elif status.status == "open":
            return HttpResponse('{"cmd": "wait", "data": "Запишите в 2 параметра"}')
        else:
            return HttpResponse('{"cmd": "xxx"}')




def Run_finger(request):

    if request.GET and "start" == request.GET["cmd"]:
        user_id = request.GET["user"]
        user_id = user_id[5:]
        FingerChangeVar("STATUS", "REC")
        FingerChangeVar("STEP", "WAIT")
        return HttpResponse("Подождите")



    elif request.GET and "stop" == request.GET["cmd"]:
        RunStop()
        return HttpResponse("Отменено")



    elif request.GET and "activ" == request.GET["cmd"]:
        user_id = request.GET["user"]
        index = request.GET["index"]
        RunActiv("finger", index)
        contact = Contact.objects.get(id = user_id)
        rfid = Rfid.objects.filter(user = user_id)
        #rf = RF.objects.filter(user = user_id)
        finger = Finger.objects.filter(user = user_id)
        return render(request, 'users/includes/user_activ.html', locals())



    elif request.GET and "delete" == request.GET["cmd"]:
        user_id = request.GET["user"]
        index = request.GET["index"]
        contact = Contact.objects.get(id = user_id)
        rfid = Rfid.objects.filter(user = user_id)
        #rf = RF.objects.filter(user = user_id)
        finger = Finger.objects.filter(user = user_id)
        RunStart(user, "finger", "delete", "no")
        RunDelete("start", index)
        return render(request, 'users/includes/own_user.html', locals())




    elif request.GET and "check" == request.GET["cmd"]:
        status = Status.objects.get(comand = "run")
        if FingerCheckVar("STATUS", "REC"):
            return HttpResponse('{"cmd": "rec", "step": "' + status.step + '"}')
        elif FingerCheckVar("STATUS", "NO"):
            return HttpResponse('{"cmd": "no", "step": "' + status.step + '", "data": "' + RunRead() + '"}')
        elif FingerCheckVar("STATUS", "TIME"):
            return HttpResponse('{"cmd": "time"}')
        elif FingerCheckVar("STATUS", "SAVE"):
            return HttpResponse('{"cmd": "save"}')
        elif FingerCheckVar("STATUS", "DELETE"):
            if FingerCheckVar("STEP", "DELETE"):
                return HttpResponse('{"cmd": "delete", "step": "delete"}')
            elif FingerCheckVar("STEP", "OK"):
                return HttpResponse('{"cmd": "delete", "step": "ok"}')
        else:
            return HttpResponse('{"cmd": "xxx", "???": "' + status.status + '"}')
