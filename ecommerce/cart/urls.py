"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from cart import views
app_name='cart'
urlpatterns = [
    path('add_to_cart/<int:pk>/',views.add_to_cart,name='add_to_cart'),
    path('cart_view/',views.cart_view,name='cart_view'),
    path('cart_decrement/<int:n>/',views.cart_decrement,name='cart_decrement'),
    path('remove/<int:p>/',views.remove,name='remove'),
    path('orderform/',views.place_order,name='orderform'),
    path('status/<u>', views.payment_status, name='payment-status'),
    path('orderview/', views.orderview, name='orderview'),


]




# 5267 3181 8797 5449  ---   master card razorpay