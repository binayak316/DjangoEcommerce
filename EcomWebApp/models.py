from email.policy import default
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    GENDER_CHOICES = (
        ('M','Male'),
        ('F','Female'),
    )
    size_choices = (
        ('7','7'),
        ('8','8'),
        ('9','9'),
        ('8.5','8.5'),
    )
    outfit_choices=(
        ('Casual','Casual'),
        ('Classic','Classic'),
    )
    name = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=100, null=True, blank=True)
    image = models.ImageField(upload_to='EcomWebApp/images', null=True, blank="True")
    price = models.FloatField()
    brand = models.CharField(max_length=100)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    size = models.CharField(max_length=10, choices=size_choices, default = '7', null= True, blank="True")
    outfit = models.CharField(max_length=10, choices=outfit_choices, default='casual')
    discount_price = models.FloatField(null=True, blank="True")
    # if the product is digital then no need to ship it if the product is not digital then it needs to be ship (ref from denis ivy)
    digital = models.BooleanField(default=False, null=True, blank=True)

    class Meta:
        ordering = ('-created_at',)


    def __str__(self):
        return self.name + self.gender
    
    @property
    def imageURL(self):
        try:
            url= self.image.url
        except:
            url= ''
        return url


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete = models.CASCADE)
    name = models.CharField(max_length=100, null = True)
    email = models.EmailField(max_length=100, null = True)

    def __str__(self):
        return self.name

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default = False, null=True,blank=False)
    transaction_id = models.CharField(max_length = 200, null=True )

    def __str__(self):
        return str(self.id)

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping = True
        return shipping   

    @property #this is for total sum of price of all products
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    @property#this property is for total cart products
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,blank=True,null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null = True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)#date_added is a date which we add item to our order

    def __str__(self):
        return str(self.product.name)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    state = models.CharField(max_length=100, null=True)
    postalcode = models.CharField(max_length=100, null=True) 
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    

