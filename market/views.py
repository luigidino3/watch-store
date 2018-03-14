from django.shortcuts import render,redirect
# Create your views here.

from .models import *
from market.forms import *
from market.forms import addItems

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

    context = {
        'all_items':all_items,
        'loggeduser':loggeduser,
        'message':message,
    }

    return render(request,'market/product.html',context)

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
            
def cart(request, user_id):
    form = creditForm(request.POST)
    all_cart = CartItem.objects.all()
    userr = User.objects.get(pk=user_id)
    cart_itemz = CartItem.objects.filter(user=userr)

    try:
        loggeduser = User.objects.get(id=request.session['user'])
        
    except(KeyError, User.DoesNotExist):
        loggeduser = 0

    if form.is_valid():
         # u no save data jus check if data valid
        transaction = Transaction()
        transaction.user = userr
        transaction.trans_date = datetime.now()
        transaction.save()

        for itemz in cart_itemz:
            trans_item = TransactionItem()
            trans_item.transaction = transaction
            trans_item.item = itemz.item
            trans_item.quantity = itemz.quantity
            trans_item.save()
            itemz.delete()
			
        return render(request, 'market/cart.html', user_id)
		
    cart_total = 0
    for itemz in cart_itemz:
        aa = (itemz.item.price * itemz.quantity)
        cart_total += aa

    context = {
		'cart_itemz':cart_itemz,
        'loggeduser':loggeduser,
        'cart_total':cart_total,
        'form':form,
	}

    return render(request,'market/cart.html',context)

def review(request):
    form = reviewForm(request.POST or None)
    context = {
        'form':form,
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

def login(request):
    all_users = User.objects.all()
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
                    elif i.accountType == 'Product Manager':
                        return redirect('prod')

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
        account.accountType = request.POST.get("accountType")
        account.firstName = "a"
        account.middleInitial = "a"
        account.lastname = "a"
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

def productDetails(request,id):
    item = Items.objects.get(pk=id)
    all_items = Items.objects.all()
    all_items = Items.objects.filter(itemtype__contains=item.itemtype)
    all_items = all_items.exclude(id__exact=item.id)
    print(item.itemtype)
    try:
        loggeduser = User.objects.get(id=request.session['user'])
    except(KeyError, User.DoesNotExist):
        loggeduser = 0

    context = {
        'item':item,
        'loggeduser':loggeduser,
        'all_items':all_items,
    }
    return render(request,'market/product-detail.html',context)

def userProfile(request, user_id):
	user = User.objects.get(pk=user_id)
	
	try:
		transactions = Transaction.objects.get(user=user)
		cart = Cart.objects.get(user=user)
	except:
		transactions = None
		cart = None
		
	all_transitems = TransactionItem.objects.all()
	
	try:
		loggeduser = User.objects.get(id=request.session['user'])
		#print('This is my session id:'+ str(request.session['user']))
	except(KeyError, User.DoesNotExist):
		loggeduser = 0
		#print("No session")
	
	context = {
		'loggeduser':loggeduser,
		'user':user,
		'transactions':transactions,
		'all_transitems':all_transitems,
	}
	
	return render(request, 'market/userprofile.html', context)

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
    }
    return render(request,'market/editprofile.html',context)
