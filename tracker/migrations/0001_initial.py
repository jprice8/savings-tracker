# Generated by Django 3.2 on 2021-04-07 21:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conversion_name', models.CharField(max_length=150)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('created_on',),
            },
        ),
        migrations.CreateModel(
            name='Facility',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('facility_number', models.CharField(max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='OldItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('imms', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=150)),
                ('poum', models.CharField(max_length=10, null=True)),
                ('uom_conv_factor', models.IntegerField(null=True)),
                ('loum', models.CharField(max_length=10)),
                ('mfr', models.CharField(max_length=100)),
                ('mfr_cat_no', models.CharField(max_length=100)),
                ('unit_cost', models.FloatField()),
                ('conversion_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.conversion')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('conversion_plan',),
            },
        ),
        migrations.CreateModel(
            name='NewItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('imms', models.CharField(max_length=10)),
                ('description', models.CharField(max_length=150)),
                ('poum', models.CharField(max_length=10, null=True)),
                ('uom_conv_factor', models.IntegerField(null=True)),
                ('loum', models.CharField(max_length=10)),
                ('mfr', models.CharField(max_length=100)),
                ('mfr_cat_no', models.CharField(max_length=100)),
                ('unit_cost', models.FloatField()),
                ('conversion_plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.conversion')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('conversion_plan',),
            },
        ),
        migrations.AddField(
            model_name='conversion',
            name='facilities',
            field=models.ManyToManyField(to='tracker.Facility'),
        ),
    ]