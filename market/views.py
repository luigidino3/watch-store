from django.shortcuts import render,redirect
# Create your views here.

from .models import *
from market.forms import *

# Get data

all_users = User.objects.all()

def home(request):
    #user_id = request.session['user']
    try:
        loggeduser = User.objects.get(id=request.session['user'])
        print('This is my session id:'+ str(request.session['user']))
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
        print("No session")

    context = {
        'loggeduser':loggeduser,
    }

    return render(request,'market/index.html',context)
'''
	try:
		loggeduser = User.objects.get(id=request.session['USERZ'])
	except (KeyError, User.DoesNotExist):
		loggeduser = 0
'''

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

        for i in all_users:
            if i.username == username:
                if i.password == password:
                    request.session['user'] = i.id
                    
                    if i.accountType == 'Customer':
                        return redirect('home')
                    elif i.accountType == 'Admin':
                        return redirect('adminPage')

        error = "Invalid username/password"

    context = {
        'error':error,
    }
    return render(request,'market/login.html',context)

def logout(request):
    del request.session['user']
    return redirect('home')

def register(request):
    form = createAccount(request.POST or None)

    if form.is_valid():
        account = form.save(commit=False)
        account.accountType = "Customer"
        account.save()
        print(account.Bcountry)
        return redirect('login')

    return render(request,'market/signup.html',{'form':form})

def admin(request):
    form = adminCreate(request.POST or None)

    if form.is_valid():
        account = form.save(commit=False)
        ### Set blank values for all fileds not needed
        #account.
        account.save()

        ##PRINT SUCCESSFULLY CREATED ACCOUNT
        ##Redirect back to admin page
        return redirect('adminPage')

    context = {
        'form':form,
    }
    return render(request,'market/adminPage.html',context)