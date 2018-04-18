from django.shortcuts import render,redirect
# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import *
from market.forms import *
from market.forms import addItems
import re
from django.views.decorators.cache import never_cache
import datetime
from django.contrib.sessions.models import Session

import logging

def ValidatingPassword(account):
	MIN_LENGTH = 8
	capital = 0
	small = 0
	message = "NO PROBLEM"
    
	# Firstname and lastname should not be allowed in password
	if account.firstName in account.password:
		message = "Firstname should not in password"
		return message
	if account.lastName in account.password:
		message = "Firstname should not in password"
		return message
	
	# At least MIN_LENGTH long
	if len(account.password) < MIN_LENGTH:
		message =  "The password must be at least %d characters long." % MIN_LENGTH 
		return message
	# At least one letter and one non-letter
	first_isalpha = account.password[0].isalpha()
	if all(c.isalpha() == first_isalpha for c in account.password):
		message = "The password must contain at least one letter and at least one digit or" \
									" punctuation character."
		return message
		
	# At least one letter is capital or small
	for c in account.password:
		if c.isalpha():
			if c == c.upper():
				capital+=1
			else:
				small+=1
	if small==0:
		message = "The password must contain at least one LowerCase Letter"
		return message
	if capital==0:
		message = "The password must contain at least one UpperCase Letter"
		return message
		
	# At least one symbol
	if all(c.isalpha() or c.isdigit() for c in account.password): 
		message = "The password must contain at least one Symbol"
		return message
		
	return message

@never_cache
def home(request):
    all_users = User.objects.all()
    #user_id = request.session['user']
    try:
        loggeduser = User.objects.get(id=request.session['user'])
        print('This is my session id:'+ str(request.session['user']))
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
        print("No session")

    all_items = Items.objects.all()
    all_items = Items.objects.order_by('quantity')[:8]
    context = {
        'loggeduser':loggeduser,
        'all_items':all_items,
    }

    return render(request,'market/index.html',context)
'''
    try:
        loggeduser = User.objects.get(id=request.session['USERZ'])
    except (KeyError, User.DoesNotExist):
        loggeduser = 0
'''

@never_cache
def shop(request):
    all_items = Items.objects.all()
    message = "All"
    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
    
    if request.method == "GET":
        if "search-product" in request.GET:
            all_items = Items.objects.filter(name__icontains=request.GET.get("search-product"))

    #if request.POST.get("addcart"):

    context = {
        'all_items':all_items,
        'loggeduser':loggeduser,
        'message':message,
    }

    return render(request,'market/product.html',context)

@never_cache
def shopAnalog(request):
    all_items = Items.objects.all()
    all_items = Items.objects.filter(itemtype__contains="Analog")
    message = "Analog"

    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
    
    if request.method == "GET":
        if "search-product" in request.GET:
            all_items = Items.objects.filter(name__icontains=request.GET.get("search-product"))

    context = {
        'all_items':all_items,
        'loggeduser':loggeduser,
        'message':message,
    }

    return render(request,'market/product.html',context)  

@never_cache
def shopDigital(request):
    all_items = Items.objects.all()
    all_items = Items.objects.filter(itemtype__contains="Digital")
    message = "Digital"

    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
    
    if request.method == "GET":
        if "search-product" in request.GET:
            all_items = Items.objects.filter(name__icontains=request.GET.get("search-product"))

    context = {
        'all_items':all_items,
        'loggeduser':loggeduser,
        'message':message,
    }

    return render(request,'market/product.html',context)  

@never_cache
def shopSmart(request):
    all_items = Items.objects.all()
    all_items = Items.objects.filter(itemtype__contains="Smart")
    message = "Smart"

    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
    
    if request.method == "GET":
        if "search-product" in request.GET:
            all_items = Items.objects.filter(name__icontains=request.GET.get("search-product"))

    context = {
        'all_items':all_items,
        'loggeduser':loggeduser,
        'message':message,
    }

    return render(request,'market/product.html',context)  

@never_cache            
def cart(request, user_id):
    form = creditForm(request.POST)
    all_cart = CartItem.objects.all()
    all_items = Items.objects.all()
    userr = User.objects.get(pk=user_id)
    cart_itemz = CartItem.objects.filter(user=userr)
    message = ""

    try:
        loggeduser = User.objects.get(id=request.session['user'])
        
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
    
    cart_total = 0
    for itemz in cart_itemz:
        aa = (itemz.item.price * itemz.quantity)
        cart_total += aa

    context = {
        'cart_itemz':cart_itemz,
        'loggeduser':loggeduser,
        'cart_total':cart_total,
        'form':form,
        'message':message,
        'userr':userr,
    }

    if request.method == "POST":
        for i in request.POST:
            print(i)
        if "buy" in request.POST:
            cvv = request.POST.get("cvv")
            num = request.POST.get("card-num")
            date = request.POST.get("date")

            if re.match(r'[0-9]{3}',cvv):
                if re.match(r'[0-9]{16}',num):
                    if date > str(datetime.date.today()):
                        for item in cart_itemz:
                            for a in all_items:
                                if item.quantity > a.quantity:
                                    message = "Insufficient stock please reduce item quantity"
                                    context = {
                                        'cart_itemz':cart_itemz,
                                        'loggeduser':loggeduser,
                                        'cart_total':cart_total,
                                        'form':form,
                                        'message':message,
                                        'userr':userr,
                                        } 
                                    return render(request,'market/cart.html',context)
                        for itemz in cart_itemz:
                            trans_item = TransactionItem()
                            trans_item.item = itemz.item
                            trans_item.quantity = itemz.quantity
                            trans_item.trans_date = datetime.date.today()
                            trans_item.user = userr
                            trans_item.save()
                            itemz.delete()
                        return redirect('history')
                        return redirect('cart',user_id=loggeduser.id)
                    else:
                        message = "Card is expired"
                        context = {
                            'cart_itemz':cart_itemz,
                            'loggeduser':loggeduser,
                            'cart_total':cart_total,
                            'form':form,
                            'message':message,
                                        'userr':userr,                            
                        }
                        return render(request,'market/cart.html',context)
                else:
                    message = "incorrect credit card number"
                    context = {
                        'cart_itemz':cart_itemz,
                        'loggeduser':loggeduser,
                        'cart_total':cart_total,
                        'form':form,
                        'message':message,
                        'userr':userr,
                                                                
                    }
                    return render(request,'market/cart.html',context)
            else: 
                message = "incorrect cvv"
                context = {
                    'cart_itemz':cart_itemz,
                    'loggeduser':loggeduser,
                    'cart_total':cart_total,
                    'form':form,
                    'message':message,
                    'userr':userr,
                }
                return render(request,'market/cart.html',context)
        else:
            for i in request.POST:
                print(i[:4])
                if i[:4] == "del-":
                    toDel = i[4:]
                    print(toDel)
                    item1 = CartItem.objects.get(id=toDel)
                    item1.delete()
                    return redirect('cart',user_id=loggeduser.id)


    return render(request,'market/cart.html',context)

@never_cache
def review(request,item_id):
    form = reviewForm(request.POST or None)
    item = Items.objects.get(id=item_id)
    checker = 0
    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0

    try:
        transactions = TransactionItem.objects.filter(user__username=loggeduser.username)
        for i in transactions:
            if i.item.name == item.name:
                checker = 1
    except(KeyError, TransactionItem.DoesNotExist):
        transactions = 0

    if request.method == "POST":
        review = form.save(commit=False)
        review.user = loggeduser
        review.item = Items.objects.get(id=item_id)
        review.save()
        return redirect('userprofile',user_id=loggeduser.id)
    context = {
        'form':form,
        'item':item,
        'loggeduser':loggeduser,
        'checker':checker,
    }
    return render(request, 'market/review.html', context)

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

@never_cache
def login(request):
    all_users = User.objects.all()
    all_counters = countess.objects.all()
    error = ''

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        for i in all_users:
            if i.username == username:
                if i.password == password:
                    
                    for a in all_counters:
                        if a.user.username == i.username:
                            if a.number >= 5:
                                error = "Your account is locked. Please contact Administrator for help"
                                return render(request,'market/login.html',{'error':error})
                            else:
                                a.number = 0
                                a.save()

                    my_old_sessions = Session.objects.all()
                    for row in my_old_sessions:
                        if row.get_decoded().get("user") == i.id:
                            row.delete()

                    request.session['user'] = i.id
                    if i.accountType == 'Customer':
                        return redirect('home')
                    elif i.accountType == 'Admin':
                        return redirect('adminPage')
                    elif i.accountType == 'Product Manager':
                        return redirect('prod')
                    elif i.accountType == 'Accounting Manager':
                        return redirect('accounting')
                else:
                    for counter in all_counters:
                        if counter.user.username == i.username:
                            counter.number += 1
                            counter.save()
                    
        error = "Invalid Username and/or Password"

    context = {
        'error':error,
    }
    return render(request,'market/login.html',context)

def logout(request):
    del request.session['user']
    return redirect('home')

@never_cache    
def register(request):
    form = createAccount(request.POST or None)
    all_users = User.objects.all()
    message = ""

    if form.is_valid():
        account = form.save(commit=False)
        account.accountType = "Customer"

        if not re.match(r"^[a-zA-z]{1,25}$",account.firstName):
            message = "Invalid first name"
            return render(request,'market/signup.html',{'form':form,'message':message}) 
        if not re.match(r"^([A-Z]{1}[.]{1})*$",account.middleInitial):
            message = "Invalid middle initial"
            return render(request,'market/signup.html',{'form':form,'message':message})
        if not re.match(r"^[a-zA-z]{1,25}$",account.lastName):
            message = "Invalid last name"
            return render(request,'market/signup.html',{'form':form,'message':message})
        if ValidatingPassword(account) != "NO PROBLEM":
            message = ValidatingPassword(account)
            return render(request,'market/signup.html',{'form':form,'message':message})
        if not re.match(r"^[A-Za-z]*$",account.Bcity):
            message = "Invalid billing city"
            return render(request,'market/signup.html',{'form':form,'message':message})
        if not re.match(r"^[A-Za-z]*$",account.Scity):
            message = "Invalid shipping city"
            return render(request,'market/signup.html',{'form':form,'message':message})
        
        username = account.username.upper()
        for i in all_users:
            temporary = i.username.upper()
            if temporary == username:
                message = "Username already taken!"
                return render(request,'market/signup.html',{'form':form,'message':message})
        account.save()
        print(account.Bcountry)
        return redirect('login')

    return render(request,'market/signup.html',{'form':form,'message':message})

@never_cache
def admin(request):
    form = adminCreate(request.POST or None)
    all_users = User.objects.all()
    message = ""

    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0

    if form.is_valid():
        if loggeduser == 0:
            return redirect('home')
        account = form.save(commit=False)
        account.accountType = request.POST.get("accountType")
        temp = account.username.upper()
        for i in all_users:
            if temp == i.username.upper():
                message = "Username already taken!!"
                return render(request,'market/adminPage.html',{"form":form,"message":message})
        account.firstName = "a"
        account.middleInitial = "a"
        account.lastName = "a"
        account.email = "a@a.com"

        account.BhouseNo = 1
        account.Bstreet = "a"
        account.Bsubdivision = "a"
        account.Bcity = "a"
        account.BpostalCode = 1
        account.Bcountry = "NZ"

        account.ShouseNo  = 1
        account.Sstreet = "a"
        account.Ssubdivision = "a"
        account.Scity = "a"
        account.SpostalCode = 1
        account.Scountry = "NZ"

        account.save()

        ##PRINT SUCCESSFULLY CREATED ACCOUNT
        ##Redirect back to admin page
        return redirect('adminPage')

    #admin_accounts = User.objects.filter(accountType__contains="Accounting Manager").filter(accountType__contains="Product Manager")
        
    context = {
        'form':form,
        'message':message,
        'all_users':all_users,
        'loggeduser':loggeduser,
    }
    return render(request,'market/adminPage.html',context)

@never_cache
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

@never_cache
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

@never_cache
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

@never_cache
def productDetails(request,id):
    item = Items.objects.get(pk=id)
    all_items = Items.objects.all()
    all_items = Items.objects.filter(itemtype__contains=item.itemtype)
    all_items = all_items.exclude(id__exact=item.id)
    all_reviews = Review.objects.all()
    all_reviews = Review.objects.filter(item=item)
    print(item.itemtype)
    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0

    if request.method == "POST":
        cart_item = CartItem()
        cart_item.quantity = request.POST.get("num-product")
        cart_item.user = loggeduser
        cart_item.item = item
        cart_item.save()

        return redirect('cart',user_id=loggeduser.id)

    context = {
        'item':item,
        'loggeduser':loggeduser,
        'all_items':all_items,
        'all_reviews':all_reviews,
    }
    return render(request,'market/product-detail.html',context)

@never_cache
def userProfile(request, user_id):
    user = User.objects.get(pk=user_id)
    
    try:
        loggeduser = User.objects.get(id=request.session['user'])
        #print('This is my session id:'+ str(request.session['user']))
    except(KeyError, User.DoesNotExist):
        loggeduser = 0
        #print("No session")
    
    context = {
        'loggeduser':loggeduser,
        'user':user,
    }
    
    return render(request, 'market/userprofile.html', context)

@never_cache
def editProfile(request,user_id):
    user = User.objects.get(id=user_id)
    form = createAccount(request.POST or None,instance=user)

    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except:
        loggeduser = 0

    if request.method == "POST":
        print("")
        if form.is_valid():
            user = form.save(commit=False)
            user.accountType = 'Customer'
            user.save()
            return redirect('userprofile',user_id=user.id)

    context = {
        'user':user,
        'form':form,
        'loggeduser':loggeduser,
    }
    return render(request,'market/editprofile.html',context)

@never_cache
def history(request):
    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except:
        loggeduser = 0

    all_items = TransactionItem.objects.all()
    all_items = TransactionItem.objects.filter(user__username__contains=loggeduser.username)

    context = {
        'all_items':all_items,
        'loggeduser':loggeduser,
    }

    return render(request,'market/history.html',context)

@never_cache
def accounting(request):
    transactions = TransactionItem.objects.all()
    all_items = Items.objects.all()
    message = 'All transactions'
    total = 0

    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0

    if request.method == "GET":
        if "all" in request.GET:
            all_items = all_items
        elif "smart" in request.GET:
            transactions = TransactionItem.objects.filter(item__itemtype__contains="Smart")
            message = 'Smart Watch transactions'
        elif "digital" in request.GET:
            transactions = TransactionItem.objects.filter(item__itemtype__contains="Digital")
            message = 'Digital Watch transactions'
        elif "analog" in request.GET:
            transactions = TransactionItem.objects.filter(item__itemtype__contains="Analog")
            message = 'Analog Watch transactions'
        elif "item" in request.GET:
            transactions = TransactionItem.objects.filter(item__name__contains=request.GET.get("item"))
            message = request.GET.get("item") + " transactions"
    
    for i in transactions:
        total = i.item.price * i.quantity + total
    context = {
        'transactions':transactions,
        'all_items':all_items,
        'message':message,
        'total':total,
        'loggeduser':loggeduser,
    }
    return render(request,'market/accounting.html',context)


def error_404(request):
        data = {}
        return render(request,'market/error_404.html', data)
 
def error_500(request):
        data = {}
        return render(request,'market/error_500.html', data)
