from django.db import models

# Create your models here.
class Order(models.Model):
    category = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    status = models.PositiveSmallIntegerField()
    def __str__(self):
        return self.name
    pass

class Delivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_name = models.CharField(max_length=255)
    start_delivery_date = models.DateTimeField('Start delivery date')
    finish_delivery_date = models.DateTimeField('Finish delivery date')
    def __str__(self):
        return self.delivery_name
    pass

class Goods(models.Model):
    goods_name = models.CharField(max_length=255)
    def __str__(self):
        return self.goods_name
    pass

class DeliveryGoods(models.Model):
    delivery = models.ForeignKey(Delivery, on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods, on_delete=models.CASCADE)
    note = models.TextField()
    def __str_(self):
        return self.delivery.delivery_name + '_' + self.goods.goods_name
    pass