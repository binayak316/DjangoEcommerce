from django.db import models

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

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.name + self.gender