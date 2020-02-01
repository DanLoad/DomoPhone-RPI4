from django.db import models
from django.contrib.auth.models import User

class Finger(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)
    number = models.DecimalField(blank=True, default=0, max_digits=15, decimal_places=0)
    finger = models.CharField(max_length = 15)
    activ = models.BooleanField(default=True)

    def __str__(self):
        return str(self.user.id)


class Var_finger(models.Model):
    name = models.CharField(unique = True, max_length = 15)
    value = models.CharField(max_length = 15)
    user = models.ForeignKey(User, blank=True, null=True, default=None, on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.name, self.value)
