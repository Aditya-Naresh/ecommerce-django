from django.db import models

# Create your models here.
class Coupon(models.Model):
    code = models.CharField(max_length=15)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.code
    
