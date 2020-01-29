from django.db import models
from users.models import Contact
from django.contrib.auth.models import User

class Rfid(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    rfid = models.CharField(max_length = 15)
    activ = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.id)
