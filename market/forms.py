from django import forms
from django.core.validators import RegexValidator
from .models import User,Items,Review, CreditInfo


class createAccount(forms.ModelForm):

    class Meta:

        model = User
        fields = ['firstName','middleInitial','lastName','username','password','email','BhouseNo','Bstreet','Bsubdivision','Bcity','BpostalCode',
        'Bcountry','ShouseNo','Sstreet','Scity','Ssubdivision','SpostalCode','Scountry']

        widgets = {
            'password':forms.PasswordInput(),
            'email':forms.EmailInput(),
            'Bstreet':forms.Textarea(),
            'Sstreet':forms.Textarea(),

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