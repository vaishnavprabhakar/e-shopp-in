from django.shortcuts import render

# # Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import UserForm, LoginForm
from django.contrib.auth import get_user_model
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
# import verify_email
from django.contrib.auth.decorators import login_required
# from django.conf import settings
# from django.core.mail import send_mail
from django.core.mail import EmailMessage
# from sms import send_sms
# from .forms import AddressForm, PasswordChangeForm
# from django.contrib.auth.forms import PasswordResetForm
# import time
# import pyotp
# import json
# import uuid
from product.models import Product, Category #Wishlist
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
# # from django.contrib.auth.tokens import default_token_generator
# from rest_framework import serializers
# from django.contrib.auth.views import PasswordResetView
# from .forms import MyPasswordResetForm
# from django.urls import reverse_lazy
User = get_user_model()
from .utils import account_activation_token
from .models import UserAddress
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models import Q
# from administration.models import Cart
# from django.http import JsonResponse


# #Create your views here.


# class MyPasswordResetView(PasswordResetView):
#     form_class = MyPasswordResetForm
#     template_name = 'password_reset.html'
#     success_url = reverse_lazy('password_reset_done')


def active(request, uidb64, token):
    User = get_user_model()

    try:
        print('++++++++++++++++++++++++++++++++++++++++++')
        uid = force_str(urlsafe_base64_decode(uidb64))
        # print(uid)
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        print('================================================')

    # checking if the user exists, if the token is valid.

    if user is not None and account_activation_token.check_token(user, token):
        # if valid set active true
        user.is_email_verified = True
        user.is_active = True
        user.save()
        messages.success(
            request,
            f"Your email has been verified successfully! You are now able to log in."
        )
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        return redirect('loginuser')
    else:
        # return HttpResponse('Activation link is invalid!')
        return render(request, 'account/active.html')


def loginuser(request):

    login_form = LoginForm()

    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            print("form is valid")
            email = login_form.cleaned_data.get('email')
            password1 = login_form.cleaned_data.get('password1')
            print(email)
            user = authenticate(email=email, password=password1)
            print(user)
            if user is not None and not user.is_superuser:
                auth_login(request, user)
                print('Redirecting to home')
                print(user.first_name + ' ' + user.last_name)
                messages.success(request, "You are successfully logged in" )
                return redirect('home')
            else:
                messages.warning(
                    request,
                    'You must create your account here..! or Check Your log in credentials.'
                )
    return render(request, 'signin.html', {'form': login_form})



@login_required(login_url='loginuser')
def home(request, category_slug=None):
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


# User Registrations with email verification using token authentication

def sign(request):
	if request.method == 'POST':
		data = request.POST
		form = UserForm(data)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = False
			user.save()
			print("Current user id", user.id)
			current_site = get_current_site(request)
			mail_subject = 'Please activate your account'
			message = render_to_string(
			    'account/email_verify.html', {
			        'user': user,
			        'domain': current_site,
			        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
			        'token': account_activation_token.make_token(user),
			    })
			to_email = form.cleaned_data.get('email')
			send_mail = EmailMessage(mail_subject, message, to=[to_email])
			send_mail.send(fail_silently=True)
			print(user.pk)
			print('user created Successfully please check the database')
			messages.success(request,
								'Your Account has been created successfuly. Please verify your email.')

		else:
			messages.success(request, 'Please checkout the inputs')
			return render(request, 'account/register.html', {'form': form})
	else:
		form = UserForm()
		messages.success(request, 'Hurryup..!')
	return render(request, 'account/register.html', {'form': form})





def profile(request):
    
    return render(request, 'account/dashboard.html')









# # @login_required(login_url='loginuser')
# def info(request):
#     if request.method == 'POST':
#         form = AddressForm(request.POST, request.FILES)
#         if form.is_valid():
#             details = UserAddress()
#             details.user = request.user
#             details.city = form.cleaned_data['city']
#             details.country = form.cleaned_data['country']
#             details.landmark = form.cleaned_data['landmark']
#             details.phone_number = form.cleaned_data['phone_number']
#             details.place = form.cleaned_data['place']
#             details.profile = form.cleaned_data['profile']
#             details.save()
#             messages.success(request, 'Address Details Added Successfully')
#             return redirect('address')
#         else:
#             messages.error(request, 'form is not valid')
#             return redirect('address')
#     else:
#         form = AddressForm()
#     return render(request, 'useraccount/detail.html', {'form': form})


def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect('loginuser')





# # @login_required(login_url='loginuser')
# def address(request):

#     return render(request, 'useraccount/address.html', {'user': user})


# # @login_required(login_url='loginuser')
# def address_show(request):

#     current_user = request.user
#     address = UserAddress.objects.filter(user=current_user)
#     paginator = Paginator(address, 3)
#     page = request.GET.get('page', 1)
#     paged_address = paginator.get_page(page)

#     return render(request, 'useraccount/profile-show.html',
#                   {'address': paged_address})



    











# @login_required(login_url='loginuser')
# def add_to_wishlist(request):
#     if request.method == 'GET':
#         prod_id = request.GET['pid']
#         product = Product.objects.get(id=prod_id)
#         user = request.user
#         Wishlist(user=user,product=product).save()
#         data = {
#             'message' : 'wishlist added successfuly',
#         }
#         return JsonResponse(data)


# @login_required(login_url='loginuser')
# def minuswishlist(request):
#     if request.method == 'GET':
#         prod_id = request.GET['pid']
#         product = Product.objects.get(id=prod_id)
#         user = request.user
#         Wishlist.objects.filter(user = user, product = product).delete()
#         data = {
#             'message' : 'wishlist remove successfuly',
#         }
#         return JsonResponse(data)