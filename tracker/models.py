from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Conversion(models.Model):
    conversion_name = models.CharField(null=False, max_length=150)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    facilities = ArrayField(models.CharField(max_length=10), blank=True)

    class Meta:
        ordering = ('-created_on',)

    def __str__(self):
        return f'{self.conversion_name}'


class OldItem(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    imms = models.CharField(null=False, max_length=10)
    description = models.CharField(null=False, max_length=150)
    poum = models.CharField(null=True, max_length=10)
    uom_conv_factor = models.IntegerField(null=True)
    luom = models.CharField(null=False, max_length=10, default="EA")
    mfr = models.CharField(null=False, max_length=100)
    mfr_cat_no = models.CharField(null=False, max_length=100)
    unit_cost = models.FloatField(null=False)
    conversion_plan = models.ForeignKey(Conversion, on_delete=models.CASCADE)

    class Meta:
        ordering = ('conversion_plan',)

    def __str__(self):
        return f'{self.description}'


class NewItem(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    imms = models.CharField(null=False, max_length=10)
    description = models.CharField(null=False, max_length=150)
    poum = models.CharField(null=True, max_length=10)
    uom_conv_factor = models.IntegerField(null=True)
    luom = models.CharField(null=False, max_length=10, default="EA")
    mfr = models.CharField(null=False, max_length=100)
    mfr_cat_no = models.CharField(null=False, max_length=100)
    unit_cost = models.FloatField(null=False)
    conversion_plan = models.ForeignKey(Conversion, on_delete=models.CASCADE)

    class Meta:
        ordering = ('conversion_plan',)

    def __str__(self):
        return f'{self.description}'

