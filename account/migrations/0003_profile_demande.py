# Generated by Django 2.0.6 on 2018-09-29 02:47

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0002_auto_20180924_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='demande',
            field=models.ManyToManyField(blank=True, related_name='in_demande', to=settings.AUTH_USER_MODEL),
        ),
    ]
