from django.shortcuts import render
from django.db.models import Q
from shop.models import Product

def search_products(request):
    P=None
    query=""
    if(request.method=="POST"):
        query=request.POST['q']
        if query:
            p=Product.objects.filter(Q(name__icontains=query)|Q(description__icontains=query))
    return render(request,'search_products.html',{'p':p,'query':query})
