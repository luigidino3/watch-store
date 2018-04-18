from django.db import models
from django_countries.fields import CountryField
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator

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

class countess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    number = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username
    
class Items(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.FloatField()

    types = (('Analog','Analog'),('Smart','Smart'),('Digital','Digital'))
    
    itemtype = models.CharField(max_length=25, choices=types, default='Analog')
    quantity = models.IntegerField()
    photo = models.ImageField(upload_to='item_photos')

    def __str__(self):
        return self.name

class TransactionItem(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Items, on_delete=models.CASCADE)
	quantity = models.IntegerField()
	trans_date = models.DateField(auto_now=False)

	def __str__(self):
		return str(self.user.username)
		
class CartItem(models.Model):
	quantity = models.IntegerField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	item = models.ForeignKey(Items, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.user.username
		
class Review(models.Model):
	title = models.CharField(max_length=120, default="A review")
	description = models.CharField(max_length=600)
	item = models.ForeignKey(Items, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	
	def __str__(self):
		return self.title

class CreditInfo(models.Model):
    cvv = models.IntegerField(validators=[MinValueValidator(3),MaxValueValidator(3)])
    cardnumber = models.IntegerField(validators=[MinValueValidator(16),MaxValueValidator(16)])
    expiration_date = models.DateTimeField(auto_now=False)

    #purpose ne2 is just for forms/validation 
    #wont save 2 da db 

    def __str__(self):
        return str(self.cardnumber)