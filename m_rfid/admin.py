from django.contrib import admin
from m_rfid.models import Rfid

class AdminRfid (admin.ModelAdmin):
    list_display = ["user","rfid","activ"]
    list_filter = ['user']

    class Meta:
        model = Rfid

admin.site.register(Rfid, AdminRfid)
