# Generated by Django 2.0.6 on 2018-10-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_onliners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onliners',
            name='intime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]