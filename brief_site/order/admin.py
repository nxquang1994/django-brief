from django.contrib import admin

# Register your models here.

from .models import Order, Delivery

admin.site.register(Order)
admin.site.register(Delivery)
