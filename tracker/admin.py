from django.contrib import admin
from .models import Conversion, OldItem, NewItem

admin.site.register(Conversion)
admin.site.register(OldItem)
admin.site.register(NewItem)