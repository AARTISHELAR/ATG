from django.contrib import admin
from Home.models import Product,Rating

# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id','product_name','price','discount','rating','global_rating']

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id','rate']

