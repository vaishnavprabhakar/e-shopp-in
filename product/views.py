from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart
from django.contrib.auth.decorators import login_required
from user.models import UserAddress, User
from django.db.models import Q
from django.http import JsonResponse
import razorpay  # razorpay integration
from django.conf import settings
from .models import Payment,Order
from django.views.decorators.cache import cache_control
# Create your views here.



def homepage(request, category_slug=None):
    categories = None
    products = None
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories,
                                          is_available=True)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = products.count()
    return render(request, 'account/home.html', {
        'products': products,
        'products_count': products_count,
    })


def product_detail(request, category_slug, product_slug):
    try:
        select_product = Product.objects.get(category__slug=category_slug,
                                             slug=product_slug)
    except Exception as e:
        raise e

    return render(request, "product_detail.html",
                  {'select_product': select_product})


@login_required(login_url='loginuser')
def add_to_cart(request):
    print('ho')
    user = request.user
    print(user)
    pid = request.GET.get('prod_id')
    print(pid)
    product = Product.objects.get(id=pid)
    print(product)
    Cart(user=user, product=product).save()
    return redirect('cart')


@login_required(login_url='loginuser')
def carth(request):
    print('hi')
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        qty = p.quantity
        discount_price = p.product.discounted_price
        print(type(qty))
        print(type(discount_price))
        value = qty * discount_price
        print('===================')
        print(value)
        amount = amount + value
    totalamount = amount + 40
    return render(request, 'account/cart.html', locals())


@login_required(login_url='loginuser')
def pluscart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required(login_url='loginuser')
def minuscart(request):
    if request.method == "GET":
        user = request.user
        prod_id = request.GET['prod_id']
        print(prod_id)
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=user))
        c.quantity -= 1
        c.save()
        #user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


@login_required(login_url='loginuser')
def removecart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.filter(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40

        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount
        }
        return JsonResponse(data)


def checkout(request):
    user = request.user
    add = UserAddress.objects.filter(user=user)
    cart_items = Cart.objects.filter(user=user)
    famount = 0
    for p in cart_items:
        value = p.quantity * p.product.discounted_price
        famount = famount + value
    totalamount = famount + 40
    razoramount = int(totalamount * 100)
    client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    print('client is authentication')
    data = {"amount": razoramount, "currency": "INR",
            "receipt": "order_rcptid_11"}
    payment_response = client.order.create(data=data)
    print(payment_response)
    order_id = payment_response['id']
    order_status = payment_response['status']
    # {'id': 'order_LuKDKFLU62oe13', 'entity': 'order', 'amount': 1004000, 'amount_paid': 0, 'amount_due': 1004000, 'currency': 'INR',
    #     'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1685111452}

    if order_status == 'created':
        print('Created')
        payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status
        )
        payment.save()
    
        
    return render(request, 'place-order.html', locals())



def paymentdone(request):
    print(request)
    order_id = request.GET.get('order_id')
    print(order_id)
    payment_id = request.GET.get('payment_id')
    print(payment_id)
    cust_id = request.GET.get('cust_id')
    print(cust_id)
    user = request.user
    print(user)
    user = User.objects.get(id=user.id)
    print(user)
    payment = Payment.objects.get(razorpay_order_id = order_id)
    print(payment.razorpay_order_id)
    payment.paid = True
    payment.razorpay_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    print(cart)
    for c in cart:
        Order(user=user, product=c.product, quantity=c.quantity, payment=payment).save()
        c.delete()
    return redirect('home')



