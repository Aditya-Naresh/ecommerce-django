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
    discount_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0) #type:ignore

    def __str__(self) -> str:
        return str(self.offer_name) + " (" + str(self.offer_type) + ")"
    
    def save(self, *args, **kwargs):
        if self.discount_rate < 0:
            self.discount_rate = 0
        super(CategoryOffer, self).save(*args, **kwargs)




class ProductOffer(models.Model):
    offer_name = models.CharField(max_length=100)
    offer_type = models.CharField(
        max_length=10,
        choices=[
            ('PERCENT', 'Percentage Discount'),
            ('FIXED', 'Fixed Amount Discount')
        ]
    )
    discount_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0) # type: ignore

    def __str__(self) -> str:
        return str(self.offer_name) + " (" + str(self.offer_type) + ")"
    
    def save(self, *args, **kwargs):
        if self.discount_rate < 0:
            self.discount_rate = 0
        super(ProductOffer, self).save(*args, **kwargs)

