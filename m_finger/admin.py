from django.contrib import admin
from m_finger.models import Finger
from m_finger.models import Var_finger

class AdminFinger (admin.ModelAdmin):
    list_display = ["user","number","finger","activ"]
    list_filter = ['user']

    class Meta:
        model = Finger

admin.site.register(Finger, AdminFinger)


class AdminVar_finger (admin.ModelAdmin):
    list_display = ["name","value", "user"]
    list_filter = ['name']

    class Meta:
        model = Var_finger

admin.site.register(Var_finger, AdminVar_finger)
