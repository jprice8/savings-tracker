# Generated by Django 3.2 on 2021-04-08 00:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20210407_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='conversion',
            name='facilities',
        ),
        migrations.AddField(
            model_name='conversion',
            name='facilities',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=10), blank=True, default=list, size=None),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Facility',
        ),
    ]
