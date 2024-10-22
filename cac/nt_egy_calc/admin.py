from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Energy

#admin.site.register(EnergyUsageNew)
admin.site.register(Energy)
    