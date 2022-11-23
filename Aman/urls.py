"""Aman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from Aman import views
from django.contrib.auth import views as auth
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('',views.home, name='home'),
    path('search',views.search, name='search'),

    path('register',views.register, name='signup'),
    path('login',views.login, name='login'),
    path('logout',views.logout, name='logout'),
    path('forgetpassword',views.forgetpassword, name='forgetpasswd'),

    path('address',views.address,name='address'),    
    path('saveaddress',views.saveaddress,name='save_address'),
    path('savepaddress',views.savepaymentaddress,name='save_p_address'),
    path('deleteaddress/<uuid:address_id>',views.deleteaddress,name='delete_address'),
    path('deletepaddress/<uuid:address_id>',views.payment_deleteaddress,name='delete_p_address'),

    path('paddress',views.payment_address,name='payment-address'), 

    path('categories/<str:categories>',views.categories, name='categories'),
    path('shop',views.shop, name='shop'),
    path('manshop',views.manshop, name='manshop'),
    path('womanshop',views.womanshop, name='womanshop'),

    path('spdpage/<uuid:product_id>',views.spdpage,name='spdpage'),
    path('podpage/<uuid:product_id>',views.podpage,name='podpage'),

    path('cart',views.cart,name='cart'),
    path('add',views.addtocart,name='addtocart'),
    path('remove/<uuid:product_id>',views.removetocart,name='removetocart'),

    path('wishlist',views.wishlist,name='wishlist'),
    path('addtowishlist',views.addtowishlist,name='addtowishlist'),
    path('removewish/<uuid:product_id>',views.removetowish,name='removetowish'),

    path('profile',views.profile,name='profile'),
    path('order',views.orders,name='order'),
    path('payment',views.payment,name='payment'),

    path('help',views.help,name='help'),
    path('aboutus',views.aboutus,name='aboutus'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)