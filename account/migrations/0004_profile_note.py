# Generated by Django 2.0.6 on 2018-10-01 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_profile_demande'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]