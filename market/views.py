from django.shortcuts import render,redirect
# Create your views here.

from .models import *
from market.forms import *
from market.forms import addItems

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
    all_items = Items.objects.all()
    form = searchForm(request.POST)

    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
    
    context = {
        'all_items':all_items,
        'form':form,
        'loggeduser':loggeduser
    }

    return render(request,'market/product.html',context)

def cart(request):
    return render(request, 'market/cart.html', context)

def about(request):
    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
    
    context = {
        'loggeduser':loggeduser,
    }
    return render(request,'market/about.html',context)

def contact(request):
    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
    
    context = {
        'loggeduser':loggeduser,
    }
    return render(request,'market/contact.html',context)

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

def productManagement(request):
    all_items = Items.objects.all()

    if request.method == "POST":
        for item in request.POST:
            if item[:7] == "delete-":
                print(item[7:])
                toDel = Items.objects.get(pk=item[7:])
                toDel.delete()
                # add successfully deleted code 
                return redirect('prod')
        

    context = {
        'all_items':all_items,
    }

    return render(request,'market/productManager.html',context)

def productManagementEdit(request,id):
    item = Items.objects.get(pk=id)
    form = uploadPhoto(request.POST,request.FILES or None,instance=item)

    if request.method == "POST":
        edited = form.save(commit=False)
        edited.name = request.POST.get("name")
        edited.description = request.POST.get("desc")
        edited.price = request.POST.get("price")
        edited.quantity = request.POST.get("quantity")
        edited.save()
        return redirect('prod')
        
    context = {
        'item':item,
        'form':form,
    }
    return render(request,'market/editItem.html',context)

def addItem(request):
    form = addItems(request.POST,request.FILES or None)

    if request.method == "POST":
        if form.is_valid():
            item = form.save(commit=False)
            #item.price = 1000.00
            item.save()
            return redirect('prod')
    
    context = {
        'form':form,
    }
    return render(request,'market/addItem.html',context)