# Generated by Django 3.2 on 2021-04-08 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_auto_20210407_2051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newitem',
            name='loum',
        ),
    ]