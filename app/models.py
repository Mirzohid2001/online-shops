from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator,MinValueValidator

# Create your models here.
STATE_CHOICES = (
    ('Toshkent','Toshkent'),
    ('Sirdayo','Sirdaryo'),
    ('Jizzax','Jizzax'),
    ('Samarqand','Samarqand'),
    ('Buxoro','Buxoro'),
    ('Qashqadaryo','Qashqadaryo'),
    ('Surxondaryo','Surxondaryo'),
    ('Navoiy','Navoiy'),
    ('Andijon','Andijon'),
    ("Farg'ona","Farg'ona"),
    ('Namangan','Namangan'),
    ('Xorazm','Xorazm'),
    ("Qoraqalpog'iston","Qoraqalpog'iston")
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)

CATEGORY_CHOICES = (
    ('M','Mobile'),
    ('L','Laptop'),
    ('TW','TopWear'),
    ('BW','BottomWear'),
)

class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField( choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.title

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

    def total_price(self):
        return self.product.selling_price * self.quantity

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delevered'),
    ('Cancel','Cansel')
)

class OrderPlaced(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quentity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Peding')


    @property
    def total_cost(self):
        return self.quentity * self.product.discounted_price


   

    




