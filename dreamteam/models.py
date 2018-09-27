from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    sendtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class Dreamteam(models.Model):
    member1 = models.OneToOneField(User, null=True, blank=True)
    member2 = models.OneToOneField(User, null=True, blank=True)
    member3 = models.OneToOneField(User, null=True, blank=True)
    member4 = models.OneToOneField(User, null=True, blank=True)
    member5 = models.OneToOneField(User, null=True, blank=True)


class Demande(models.Model):
    dreamteam = models.OneToOneField(Dreamteam)
    sendings = models.ManyToManyField(User, null=True, blank=True)

class Accept(models.Model):
    dreamteam = models.OneToOneField(Dreamteam)
    accept = models.BooleanField(default=False)
    accepter = models.ForeignKey(User)