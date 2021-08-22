from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length = 500)
    price = models.DecimalField(max_digits = 6,decimal_places = 1,null=True)
    discount = models.CharField(max_length = 50,null = True)
    image = models.URLField(max_length = 500,null = True)
    global_rating = models.PositiveIntegerField(null=True)
    rating = models.ForeignKey('Rating',on_delete = models.CASCADE)
    def __str__(self):
        return self.product_name

class Rating(models.Model):
    rate = models.DecimalField(max_digits = 2 ,decimal_places = 1,null = True)
    def __str__(self):
        return str(self.rate)