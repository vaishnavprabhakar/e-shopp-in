from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart, Wishlist
from django.contrib.auth.decorators import login_required
from user.models import UserAddress, User
from django.db.models import Q
from django.http import JsonResponse
import razorpay  # razorpay integration
from django.conf import settings
from .models import Payment, Order, Wishlist
from django.views.decorators.cache import cache_control
# Create your views here.


# @login_required(login_url='loginuser')
def search(request):
    category = Category.objects.all()
    product = Product.objects.all()
    product = None
    if 'search' in request.GET:
        search = request.GET.get('search')
        if 'search':
            product = Product.objects.order_by('-created_date').filter(
                Q(description__icontains=search) | Q(product_name__icontains=search))
        else:
            return redirect('home')
    context = {
        'category': category,
        'product': product,

    }
    return render(request, 'search.html', context)



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
        products = Product.objects.all().filter()
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
    user = request.user
    pid = request.GET.get('prod_id')
    product = get_object_or_404(Product, id=pid)
    cart_item, created = Cart.objects.get_or_create(user=user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')


@login_required(login_url='loginuser')
def carth(request):
    print('hi')
    user = request.user
    cart = Cart.objects.filter(user=user)
    product_count = cart.count()
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
        print(data)
        return JsonResponse(data)


@login_required(login_url='loginuser')
def minuscart(request):
    if request.method == "GET":
        user = request.user
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=user))
        if c.quantity >= 2:
            c.quantity -= 1
        c.save()
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

        if cart.exists():
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
        else:
            data = {'refresh': True}
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

    data = {"amount": razoramount, "currency": "INR",
            "receipt": "order_rcptid_11"}

    payment_response = client.order.create(data=data)

    order_id = payment_response['id']

    order_status = payment_response['status']
    # {'id': 'order_LuKDKFLU62oe13', 'entity': 'order', 'amount': 1004000, 'amount_paid': 0, 'amount_due': 1004000, 'currency': 'INR',
    #     'receipt': 'order_rcptid_11', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1685111452}

    if order_status == 'created':

        payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status=order_status
        )

        payment.save()

    return render(request, 'place-order.html', locals())


def paymentdone(request):
    try:
        order_id = request.GET.get('order_id')
        payment_id = request.GET.get('payment_id')
        cust_id = request.GET.get('cust_id')

        user = request.user
        user = get_object_or_404(User, id=cust_id)
        payment = get_object_or_404(Payment, razorpay_order_id=order_id)

        payment.paid = True
        payment.razorpay_payment_id = payment_id
        payment.save()

        cart = Cart.objects.filter(user=user)
        for c in cart:
            Order(user=user,product=c.product, quantity=c.quantity, payment=payment).save()
            c.delete()
        return redirect("orders")

    except (User.DoesNotExist, Payment.DoesNotExist):
        return redirect("orders")
    except Exception as e:      
        print(str(e))
        return redirect("orders")


# order done

@login_required(login_url='loginuser')
def orders(request):
    user = request.user
    totalitem = 0
    wishitem = 0
    totalitem = Cart.objects.filter(user=request.user).count()
    wishitem = int(Wishlist.objects.filter(user=request.user).count())
    orders = Order.objects.filter(user=request.user)
    return render(request, 'payment_done.html', locals())


# wishlist funstion


@login_required(login_url='loginuser')
def add_to_wishlist(request):
    
    if request.method == 'GET':
        prod_id = request.GET.get('pid')
        product = Product.objects.get(id=prod_id)
        user = request.user
        wishitem, created = Wishlist.objects.get_or_create(user=user, product=product)
        print(created, wishlist)
        if created:
            data = {
                'message': 'Wishlist added successfully',
            }
        else:
            data = {
                'message': 'Wishlist already exists',
            }

        return JsonResponse(data)