from django.contrib import admin

# Register your models here.

from .models import Order, Delivery, Goods, DeliveryGoods

admin.site.register(Order)
admin.site.register(Delivery)
admin.site.register(Goods)
admin.site.register(DeliveryGoods)

