from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Dreamteam(models.Model):
    member1 = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='member1')
    member2 = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='member2')

    def __str__(self):
        r = '{0} et {1}'.format(self.member1, self.member2)
        return r


class Chat(models.Model):
    dreamteam = models.ForeignKey(Dreamteam, on_delete=models.CASCADE, null=True)
    comefrom = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='comefrom')
    to = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='cometo')
    message = models.TextField()
    unread = models.BooleanField(default=False)
    sendtime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    def destinateur(self):
        return self.comefrom

    class Meta:
        ordering = ['sendtime']
