from django.db import models
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from djmoney.money import Money

# Create your models here.
class User(models.Model):

    accounts = (
        ('Customer','Customer'),
        ('Product Manager','Product Manager'),
        ('Accounting Manager','Accounting Manager'),
        ('Admin','Admin'),
    )

    #Basic Details
    accountType = models.CharField(max_length=25,choices=accounts,default='Customer')
    firstName = models.CharField(max_length=25)
    middleInitial = models.CharField(max_length=10)
    lastName = models.CharField(max_length=25)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.CharField(max_length=25)

    #Billing Details
    BhouseNo = models.IntegerField()
    Bstreet = models.CharField(max_length=50)
    Bsubdivision = models.CharField(max_length=50)
    Bcity = models.CharField(max_length=50)
    BpostalCode = models.IntegerField()
    Bcountry = CountryField()

    #Shipping Details
    ShouseNo = models.IntegerField()
    Sstreet = models.CharField(max_length=50)
    Ssubdivision = models.CharField(max_length=50)
    Scity = models.CharField(max_length=50)
    SpostalCode = models.IntegerField()
    Scountry = CountryField()

    def __str__(self):
        return self.username

class Items(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    #price = MoneyField(max_digits=20, decimal_places=2, default_currency='PHP')
    price = models.FloatField()

    types = (('Analog','Analog'),('Smart','Smart'),('Digital','Digital'))
    
    itemtype = models.CharField(max_length=25, choices=types, default='Analog')
    quantity = models.IntegerField(default=20)
    photo = models.ImageField(upload_to='item_photos')

    def __str__(self):
        return self.name
