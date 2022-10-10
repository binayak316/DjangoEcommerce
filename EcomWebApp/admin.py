from django.contrib import admin
from EcomWebApp.models import Product

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','brand', 'price')

admin.site.register(Product,ProductAdmin)