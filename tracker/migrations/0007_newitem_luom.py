# Generated by Django 3.2 on 2021-04-08 01:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0006_remove_newitem_loum'),
    ]

    operations = [
        migrations.AddField(
            model_name='newitem',
            name='luom',
            field=models.CharField(default='EA', max_length=10),
        ),
    ]