from django.contrib import admin
from EcomWebApp.models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=('name','brand', 'price')

admin.site.register(Product,ProductAdmin)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)

