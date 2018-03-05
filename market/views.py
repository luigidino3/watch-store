from django.shortcuts import render,redirect
# Create your views here.

from .models import User
from market.forms import createAccount

# Get data

all_users = User.objects.all()

def home(request):
    return render(request,'market/index.html',{})

def shop(request):
    return render(request,'market/product.html',{})

def about(request):
    return render(request,'market/about.html',{})

def contact(request):
    return render(request,'market/contact.html',{})

def login(request):
    error = ''

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        print(username)
        print(password)

        for i in all_users:
            if i.username == username:
                if i.password == password:
                    request.session['user'] = i.username
                    return redirect('home')

        error = "Invalid username/password"

    context = {
        'error':error,
    }
    return render(request,'market/login.html',context)

def register(request):
    form = createAccount(request.POST)

    return render(request,'market/signup.html',{'form':form})