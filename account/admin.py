from django.contrib import admin

# Register your models here.
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Profile)
admin.site.register(models.Following)
admin.site.register(models.Publication)
admin.site.register(models.Comments)
admin.site.register(models.Notification)
admin.site.register(models.User_groups)
admin.site.register(models.Onliners)
admin.site.register(models.Message)