from django.db import models

# Create your models here.
class CategoryOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    offer_type = models.CharField(
        max_length=10,
        choices=[
            ('PERCENT', 'Percentage Discount'),
            ('FIXED', 'Fixed Amount Discount')
        ]
    )
    discount_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return str(self.offer_name) + " (" + str(self.offer_type) + ")"
    




class ProductOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    offer_type = models.CharField(
        max_length=10,
        choices=[
            ('PERCENT', 'Percentage Discount'),
            ('FIXED', 'Fixed Amount Discount')
        ]
    )
    discount_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self) -> str:
        return str(self.offer_name) + " (" + str(self.offer_type) + ")"