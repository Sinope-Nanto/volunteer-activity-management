# Generated by Django 3.2.9 on 2021-11-30 07:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_auto_20211129_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken',
            name='end',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 30, 15, 57, 22, 40486)),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='start',
            field=models.DateTimeField(default=datetime.datetime(2021, 11, 30, 15, 57, 22, 40486)),
        ),
    ]