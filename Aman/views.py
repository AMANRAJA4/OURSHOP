from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  
from django.db.models import Q
from django.core.mail import send_mail

from django.conf import settings
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
from Tables.models import ADDRESS,BRAND,CATEGORIES,CART,COLOUR,PRODUCT,ORDER,WISHLIST


def home(request):

    man = PRODUCT.objects.filter(gender='Man')
    paginator=Paginator(man,4)
    page_number=request.GET.get('page')
    man=paginator.get_page(page_number)

    woman = PRODUCT.objects.filter(gender='Woman')
    paginator=Paginator(woman,4)
    page_number=request.GET.get('page')
    woman=paginator.get_page(page_number)

    shirt = CATEGORIES.objects.filter(categories='Shirt')
    jeans = CATEGORIES.objects.filter(categories='Jeans')
    trouser = CATEGORIES.objects.filter(categories='Trousers')
    trackpant = CATEGORIES.objects.filter(categories='Trackpants')
    shoes = CATEGORIES.objects.filter(categories='Shoes')
    wallet = CATEGORIES.objects.filter(categories='Wallet')
    watch = CATEGORIES.objects.filter(categories='Watch')
    formal_suit = CATEGORIES.objects.filter(categories='Formal suit')

    top_jeans = CATEGORIES.objects.filter(categories='Top jeans')
    tops = CATEGORIES.objects.filter(categories='Tops')
    salwar_suit = CATEGORIES.objects.filter(categories='Salwar suit')
    frock = CATEGORIES.objects.filter(categories='Frock')

    return render(request, "Home.html",{'man':man,'woman':woman,'shirt':shirt,'jeans':jeans,'trouser':trouser,'trackpant':trackpant,'shoes':shoes,'wallet':wallet,'watch':watch,'formal_suit':formal_suit,'top_jeans':top_jeans,'tops':tops,'salwar_suit':salwar_suit,'frock':frock})

def search(request):
    if request.method== 'POST':
        search = request.POST.get('search_value')
        results = PRODUCT.objects.filter(Q(product_name__icontains=search) | Q(gender__icontains=search) | Q(categories__categories=search)| Q(colour__colour_name=search))
        data={'searchresult':results}
        return render(request, "Search-products.html",data)
    return redirect('home')

def shop(request):

    shirt = CATEGORIES.objects.filter(categories='Shirt')
    jeans = CATEGORIES.objects.filter(categories='Jeans')
    trouser = CATEGORIES.objects.filter(categories='Trousers')
    trackpant = CATEGORIES.objects.filter(categories='Trackpants')
    shoes = CATEGORIES.objects.filter(categories='Shoes')
    wallet = CATEGORIES.objects.filter(categories='Wallet')
    watch = CATEGORIES.objects.filter(categories='Watch')
    formal_suit = CATEGORIES.objects.filter(categories='Formal suit')

    top_jeans = CATEGORIES.objects.filter(categories='Top jeans')
    tops = CATEGORIES.objects.filter(categories='Tops')
    salwar_suit = CATEGORIES.objects.filter(categories='Salwar suit')
    frock = CATEGORIES.objects.filter(categories='Frock')

    categories_product = PRODUCT.objects.filter(categories__categories = categories)
    data = {'categories_product':categories_product,'shirt':shirt,'jeans':jeans,'trouser':trouser,'trackpant':trackpant,'shoes':shoes,'wallet':wallet,'watch':watch,'formal_suit':formal_suit,'top_jeans':top_jeans,'tops':tops,'salwar_suit':salwar_suit,'frock':frock}
    return render(request, "Shop-page.html",data)

def categories(request,categories):
    categories_name = categories
    categories_product = PRODUCT.objects.filter(categories__categories = categories)
    data = {'categories_product':categories_product,'categories_name':categories_name}
    return render(request, "Categories-item.html",data)

def manshop(request):
    man = PRODUCT.objects.filter(gender='Man')
    data = {'man_products':man}
    return render(request, "Man-shop.html",data)

def womanshop(request):
    woman = PRODUCT.objects.filter(gender='Woman')
    data = {'woman_products':woman}
    return render(request, "Woman-shop.html",data)

def spdpage(request,product_id):
    single_product_dtls = PRODUCT.objects.filter(product_id = product_id)
    data = {'S_P_dtls':single_product_dtls}
    return render(request,"spdpage.html",data)

def wishlist(request):
    if request.user.is_authenticated:
        user = request.user
        wishlist = WISHLIST.objects.filter(user=user)
        data={'wishlist_product':wishlist}
        return render(request,'wishlist.html',data)
    return render(request, "First-login.html")

def addtowishlist(request):
    if request.user.is_authenticated:
        user = request.user
        product_id= request.POST['product_id']
        product = PRODUCT.objects.get(product_id=product_id)
        if WISHLIST.objects.filter(product_id=product_id).exists():
            return redirect('wishlist')
        else:
            WISHLIST(user=user, product=product).save()
            return redirect('wishlist')
    else:
        return render(request,"First-login.html")

def removetowish(request,product_id):
    user=request.user
    wishlist=WISHLIST.objects.filter(product__product_id=product_id)
    wishlist.delete()
    return redirect('wishlist')

def cart(request):
    if request.user.is_authenticated:
        user = request.user
        address = ADDRESS.objects.filter(user=user)
        cart = CART.objects.filter(user=user)
        amount =0.0
        shipping_amount =100.00
        total_amount = 0.0
        cart_product = [p for p in CART.objects.all() if p.user==user]

        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.selling_price)
                amount +=tempamount
                total_amount = amount + shipping_amount
            return render(request,'cart.html',{'carts':cart,'amount':amount,'total_amount':total_amount,'shipping_amount':shipping_amount,'address':address})
        else:
            return render(request,'Empty-cart.html')
    return render(request, "First-login.html")

def addtocart(request):
    if request.user.is_authenticated:
        user = request.user
        product_id= request.POST['product_id']

        product = PRODUCT.objects.get(product_id=product_id)

        if CART.objects.filter(product_id=product_id).exists():
            return redirect('cart')
        else:
            CART(user=user, product=product).save()
            return redirect('cart')
    else:
        return render(request,"First-login.html")

def removetocart(request,product_id):
    user=request.user
    cart=CART.objects.filter(product__product_id=product_id)
    cart.delete()
    return redirect('cart')

def register(request):

    if request.method=="POST":
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        email=request.POST['email']
        password=request.POST['password']

        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already taken. Please try another email.")
            return redirect('signup')
        else:
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=email,email=email,password=password)
            user.save()

            #subject='OURSHOP'
            #message=f'Welcome {first_name} to register your self in oushop.com.'
            #email_from=settings.EMAIL_HOST_USER
            #recipient_list=[email,]
            #send_mail(
            #    'OURSHOP',
            #    'Welcome ADMIN to register your self in oushop.com.',
            #    'settings.EMAIL_HOST_USER',
            #    [email],
            #    fail_silently=False)
        
            messages.success(request, "You have Successfully Registered.")
            return redirect('login')

    return render(request, "register.html")

def login(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = auth.authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            auth.login(request,user)
            messages.success(request, "Successfully loged in")
            return redirect('home')
        else:
            messages.warning(request, "Username or password is wrong. Please try again")
            return redirect('login')

    return render(request, "login.html")

def logout(request):
        auth.logout(request)
        messages.success(request, "Successfully loged out")
        return redirect('home')

def forgetpassword(request):
    return render(request, "forget.html")

def address(request):
    if request.user.is_authenticated:
        address = ADDRESS.objects.filter(user=request.user)
        return render(request,'address.html',{'address':address})
    return render(request, "First-login.html")

def add_new_address(request):
    if request.user.is_authenticated:
        user = request.user
        address = ADDRESS.objects.filter(user=user)
        all_addresses = [p for p in ADDRESS.objects.all() if p.user==user]

        return render(request,'address.html',{'alladdress':all_addresses})
    return render(request, "First-login.html")

def saveaddress(request):
    user = request.user
    if request.method=="POST":
        mobile=request.POST['mobile']
        state=request.POST['state']
        city=request.POST['city']
        pincode=request.POST['pincode']

        user = ADDRESS(user=user,mobile=mobile,state=state,city=city,zipcode=pincode)
        user.save()

        messages.success(request, "Successfully save address.")
        return redirect('address')

def savepaymentaddress(request):
    user = request.user
    if request.method=="POST":
        mobile=request.POST['mobile']
        state=request.POST['state']
        city=request.POST['city']
        pincode=request.POST['pincode']

        user = ADDRESS(user=user,mobile=mobile,state=state,city=city,zipcode=pincode)
        user.save()

        messages.success(request, "Successfully save address.")
        return redirect('payment-address')

def deleteaddress(request,address_id):
    user=request.user
    address=ADDRESS.objects.filter(address_id=address_id)
    address.delete()
    return redirect('address')

def payment_address(request):
    if request.user.is_authenticated:
        address = ADDRESS.objects.filter(user=request.user)
        if address is not None:
            return render(request,'payment-address.html',{'address':address})
        
def payment_deleteaddress(request,address_id):
    user=request.user
    address=ADDRESS.objects.filter(address_id=address_id)
    address.delete()
    return redirect('payment-address')

def profile(request):
    if request.user.is_authenticated:
        user=request.user
        address = ADDRESS.objects.filter(user=user)
        data={'address':address,'user':user}
        return render(request,'Profile.html',data)
    return render(request, "First-login.html")

def orders(request):
    user=request.user
    user_order = ORDER.objects.filter(user=user)
    data={'user_order':user_order}
    return render(request,'PlacedOrder.html',data)

def podpage(request,product_id):
    user=request.user
    ordered_product_dtls = ORDER.objects.filter(product_id = product_id)
    data = {'O_P_dtls':ordered_product_dtls}
    return render(request,"OrderDetailedPage.html",data)

def payment(request):
    user=request.user
    custid = request.GET.get('address_id')
    address=ADDRESS.objects.get(address_id=custid)
    cart=CART.objects.filter(user=user)
    for c in cart:
        order = ORDER(user=user,address=address,product=c.product,quantity=c.quantity).save()
        c.delete()
    return redirect('order')


def help(request):
    return render(request,"help.html")

def aboutus(request):
    return render(request,"aboutus.html")