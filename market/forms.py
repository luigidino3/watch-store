from django import forms
from django.core.validators import RegexValidator
from .models import User,Items,Review, CreditInfo


class DateInput(forms.DateInput):
    input_type = 'date'

class createAccount(forms.ModelForm):

    class Meta:

        model = User
        fields = ['firstName','middleInitial','lastName','username','email','BhouseNo','Bstreet','Bsubdivision','Bcity','BpostalCode',
        'Bcountry','ShouseNo','Sstreet','Scity','Ssubdivision','SpostalCode','Scountry','password']

        widgets = {
            'password':forms.PasswordInput(),
            'email':forms.EmailInput(),
            'Bstreet':forms.Textarea(),
            'Sstreet':forms.Textarea(),

        }

        labels = {
            'firstName': ('First Name'),
            'middleInitial': ('Middle Initial'),
            'lastName': ('Last Name'),
            'username': ('Username'),
            'email': ('Email Address'),
            'BhouseNo': ('Billing House'),
            'Bstreet': ('Billing Street'),
            'Bsubdivision': ('Billing Subdivision'),
            'Bcity': ('Billing City'),
            'BpostalCode': ('Billing Postal Code'),
            'Bcountry': ('Billing Country'),
            'ShouseNo': ('Shipping House No.'),
            'Sstreet': ('Shipping Street'),
            'Scity': ('Shipping City'),
            'Ssubdivision': ('Shipping Subdivision'),
            'SpostalCode': ('Shipping Postal Code'),
            'Scountry': ('Shipping Country'),
            'password': ('Password'),
        }

class adminCreate(forms.ModelForm):

    class Meta:

        model = User
        fields = ['username','password']

        widgets = {
            'password':forms.PasswordInput(),
        }

class uploadPhoto(forms.ModelForm):

    class Meta:

        model = Items
        fields = ['photo']

class searchForm(forms.ModelForm):
	
	class Meta:
	
		model = Items
		fields = ['name']

class addItems(forms.ModelForm):

    class Meta:

        model = Items
        fields = ['name','description','price','itemtype','quantity','photo']
        widgets = {
            'description':forms.Textarea(),
        }

class reviewForm(forms.ModelForm):

	class Meta:
	
		model = Review
		fields = ['title', 'description']

class creditForm(forms.ModelForm):

    class Meta:

        model = CreditInfo
        fields = ['cvv', 'cardnumber', 'expiration_date']

        widgets = { 'expiration_date':DateInput() }

class changePass(forms.ModelForm):

    class Meta:

        model = User
        fields = ['password']

        labels = {'password': ('New Password'), }