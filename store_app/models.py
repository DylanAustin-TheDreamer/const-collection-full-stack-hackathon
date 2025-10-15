from django.db import models


# Add product models here
class Order(models.Model):
    order_id = models.IntegerField()
    buyer_id = models.IntegerField()
    artwork_id = models.IntegerField()
    order_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'), ('shipped', 'Shipped'), ('delivered', 'Delivered')], default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2)