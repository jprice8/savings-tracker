# Generated by Django 3.2 on 2021-04-08 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='po',
            name='po_date',
            field=models.DateField(),
        ),
    ]
