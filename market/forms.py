from django import forms
from django.core.validators import RegexValidator
from .models import User,Items


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