from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms import ModelForm

from .models import Conversion, OldItem, NewItem 


class OldItemForm(ModelForm):
    class Meta:
        model = OldItem
        fields = [
            'imms',
            'description',
            'poum',
            'uom_conv_factor',
            'luom',
            'mfr',
            'mfr_cat_no',
            'unit_cost',
        ]


class NewItemForm(ModelForm):
    class Meta:
        model = NewItem
        fields = [
            'imms',
            'description',
            'poum',
            'uom_conv_factor',
            'luom',
            'mfr',
            'mfr_cat_no',
            'unit_cost',
        ]

