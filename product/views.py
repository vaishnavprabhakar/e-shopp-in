from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Category,Cart
from django.contrib.auth.decorators import login_required
from user.models import UserAddress
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.


@login_required(login_url='loginuser')
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
        select_product = Product.objects.get(category__slug = category_slug,
                                             slug = product_slug)
    except Exception as e:
        raise e

    return render(request, "product_detail.html",
                  {'select_product': select_product})




# @login_required(login_url='loginuser')
def add_to_cart(request):
    print('ho')
    user =  request.user
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
    amount= 0
    for p in cart:
        qty = p.quantity
        discount_price = p.product.discounted_price
        print(type(qty))
        print(type(discount_price))
        value = qty * discount_price
        print('===================')
        print(value)
        amount  = amount + value    
    totalamount = amount + 40
    return render(request, 'account/cart.html',locals())




@login_required(login_url='loginuser')
def pluscart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
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
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
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
def removecart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
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
    return render(request, 'place-order.html',locals())