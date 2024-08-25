from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from shop.models import Product
from cart.models import Cart,Payment,Order_table
from django.http import HttpResponse
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

# cart view

@login_required
def add_to_cart(request,pk):
    p=Product.objects.get(id=pk)
    u=request.user
    try:
        cart=Cart.objects.get(user=u,product=p)
        if(p.stock>0):
            cart.quantity += 1
            cart.save()
            p.stock -= 1
            p.save()
    except:
        if(p.stock):
            cart = Cart.objects.create(product=p,user=u,quantity=1)
            cart.save()
            p.stock -= 1
            p.save()

    return redirect("cart:cart_view")

@login_required
def cart_view(request):
    u=request.user
    cart=Cart.objects.filter(user=u)
    total=0
    for i in cart:
        total=total+i.quantity*i.product.price

    return render(request,'cart.html',{'cart':cart,'total':total})
def cart_decrement(request,n):
    p = Product.objects.get(id=n)
    u = request.user
    try:
        cart = Cart.objects.get(user=u,product=p)
        if(cart.quantity>1):
            cart.quantity -=1
            cart.save()
            p.stock +=1
            p.save()
        else:
            cart.delete()
            p.stock +=1
            p.save()

    except:
        pass
    return redirect("cart:cart_view")


def remove(request,p):
    p = Product.objects.get(id=p)
    u = request.user
    try:
        cart = Cart.objects.get(user=u,product=p)
        cart.delete()
        p.stock += cart.quantity
        p.save()
    except:
        pass
    return redirect("cart:cart_view")


def place_order(request):
    if(request.method=="POST"):
        phone=request.POST.get('phone')
        address = request.POST.get('address')
        pin = request.POST.get('pin')
        u = request.user
        c = Cart.objects.filter(user=u)
        total=0
        for i in c:
            total=total+i.quantity*i.product.price     #total amount
            total=int(total*100)  #  converse the total rs to paisa

    # create Razorpay client using our api credentials

        client=razorpay.Client(auth=('rzp_test_aIhVsjMpWirXq5','JCKiwFJpbjZQ2X6cNthM199F'))      #create a client in razorpay

        # create order in Razorpay
        response_payment=client.order.create(dict(amount=total,currency='INR'))
        print(response_payment)
        order_id=response_payment['id']
        order_status=response_payment['status']
        if order_status=="created":
            p=Payment.objects.create(name=u.username,amount=total,order_id=order_id)    #save the payment details in Payment table
            p.save()
            for i in c:
                o = Order_table.objects.create(user=u, product=i.product, address=address, phone=phone, pin=pin, no_of_items=i.quantity, order_id=order_id)
                o.save()

        response_payment['name']=u.username
        return render(request, 'payment.html',{'payment':response_payment})

    return render(request,'orderform.html')

@csrf_exempt
def payment_status(request,u):
    print(request.user.is_authenticated)  #false
    if not request.user.is_authenticated:
        user = User.objects.get(username=u)
        login(request,user)
        print(request.user.is_authenticated)  #true

    if(request.method=="POST"):
        username=request.user
        print(username)
        response = request.POST  #Razorpay response after completion of payment
        print(response)
        print(u)

        param_dict = {
            'razorpay_order_id': response['razorpay_order_id'],
            'razorpay_payment_id': response['razorpay_payment_id'],
            'razorpay_signature': response['razorpay_signature'],
        }
        client=razorpay.Client(auth=('rzp_test_aIhVsjMpWirXq5','JCKiwFJpbjZQ2X6cNthM199F'))      #create a client in razorpay
        try:
            status = client.utility.verify_payment_signature(param_dict)    # To check the authenticity of razorpay signature
            print(status)

            # After successful payment

            # Retrieve a payment record with particular order_id

            ord = Payment.objects.get(order_id=response['razorpay_order_id'])
            ord.razorpay_payment_id = response['razorpay_payment_id'] #edits payment id response['razorpay_payment_id']
            ord.paid = True  #edit paid to True
            ord.save()

            u=User.objects.get(username=u)
            c=Cart.objects.filter(user=u)

            # filter the order_table details for particular user with order_id =response['razorpay_order_id']
            o=Order_table.objects.filter(user=u,order_id=response['razorpay_order_id'])
            for i in o:
                i.payment_status="paid"  #edits payment status="paid"
                i.save()

                c.delete()   #Deletes the cart items for particular user
                return render(request, 'payment_status.html', {'status': True})

        except:
            return render(request,'payment_status.html',{'status':False})

    return render(request,'payment_status.html')




@login_required
def orderview(request):
    u=request.user
    orders=Order_table.objects.filter(user=u,payment_status="paid")


    return render(request,'orderview.html',{'orders':orders,'u':u.username})