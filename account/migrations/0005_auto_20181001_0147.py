# Generated by Django 2.0.6 on 2018-10-01 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_profile_note'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='address',
        ),
        migrations.AddField(
            model_name='profile',
            name='sexe',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
