from django.db import models
from users.models import Contact
from django.contrib.auth.models import User

class Rfid(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    rfid = models.CharField(max_length = 15)
    activ = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.id)

class Var_rfid(models.Model):
    name = models.CharField(unique = True, max_length = 15)
    value = models.CharField(max_length = 15)
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.name, self.value)
