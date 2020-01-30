from django.contrib import admin
from m_rfid.models import Rfid
from m_rfid.models import Var_rfid

class AdminRfid (admin.ModelAdmin):
    list_display = ["user","rfid","activ"]
    list_filter = ['user']

    class Meta:
        model = Rfid

admin.site.register(Rfid, AdminRfid)


class AdminVar_rfid (admin.ModelAdmin):
    list_display = ["name","value", "user"]
    list_filter = ['name']

    class Meta:
        model = Var_rfid

admin.site.register(Var_rfid, AdminVar_rfid)
