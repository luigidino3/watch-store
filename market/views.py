from django.shortcuts import render

# Create your views here.

from .models import User

def home(request):
    return render(request,'market/index.html',{})

def shop(request):
    return render(request,'market/product.html',{})

def about(request):
    return render(request,'market/about.html',{})

def contact(request):
    return render(request,'market/contact.html',{})