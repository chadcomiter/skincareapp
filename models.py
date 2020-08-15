from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


##Declares Product
class Product(models.Model):
    ##Fields
    name = models.CharField(max_length = 200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    breakout = models.BooleanField(default=False)

    ##Renames the instance of the model with it's name
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    product = models.ForeignKey(Product, related_name="ingredients", verbose_name="product", on_delete=models.CASCADE)

    def __str__(self):
        return self.product.name + " - " + self.name