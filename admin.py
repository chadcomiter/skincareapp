from django.contrib import admin
from .models import Product
from .models import Ingredient

admin.site.register(Product)
admin.site.register(Ingredient)