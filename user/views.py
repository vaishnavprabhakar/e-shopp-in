from django.shortcuts import render
from django.shortcuts import reverse
# # Create your views here.

from django.http import HttpResponse
from . forms import UserForm, LoginForm, UpdateAddressForm, UpdateProfileForm, UpdateUserForm
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from .utils import account_activation_token
from product.models import Product, Category, Wishlist, Order
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError

from .models import UserAddress, User, Profile
from product.models import Order, Cart, Wishlist

from django.views.decorators.cache import cache_control
# #Create your views here.


# class MyPasswordResetView(PasswordResetView):
#     form_class = MyPasswordResetForm
#     template_name = 'password_reset.html'
#     success_AttributeError: 'str' objects has no attribute 'get'url = reverse_lazy('password_reset_done')

User = get_user_model()

def active(request, uidb64, token):

    try:
      
        uid = force_str(urlsafe_base64_decode(uidb64))
      
        user = User.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
      

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
        return reverse('loginuser')
        # messages.success(request, 'You can now login to your account.Thank U')
    else:
        # messages.warning(request, 'Your account activation token has been expired')
        return render(request, 'account/active.html')



def loginuser(request):
        
    login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(email=email, password=password1)
            if user is not None and not user.is_superuser:
                auth_login(request, user)
                messages.success(request, "You are successfully logged in")
                return redirect('home')
            else:
                messages.success(
                    request,
                    'You must create your account here..! or Check Your log in credentials.'
                )
    return render(request, 'signin.html', {'form': login_form})


@login_required(login_url='login/')
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
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sign(request):
    
    if request.method == 'POST':
        data = request.POST
        form = UserForm(data)
        print(form)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            
            user.save()
           
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
           
           
            messages.success(request,
                             'Your Account has been created successfuly. Please verify your email.')

        else:
            messages.success(request, 'Please checkout the inputs, or create another email that you are using.')
            return render(request, 'account/register.html', {'form': form})
    else:
        form = UserForm()
        messages.success(request, 'Hurryup..!')
    return render(request, 'account/register.html', {'form': form})


@login_required(login_url='/login')
def profile(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'account/dashboard.html', context)


@login_required(login_url='loginuser')
def edit_profile(request):
    user = request.user
    try:
        user = request.user
        user_obj = get_object_or_404(User, email= user.email)
        userform = UpdateUserForm(instance=user_obj)
        addform = UpdateAddressForm(instance=user_obj)
        profileform = UpdateProfileForm(instance=user_obj)
    except User.DoesNotExist:
        pass
    if request.method == 'POST':
        userform = UpdateUserForm(request.POST , instance=request.user)
        profileform = UpdateProfileForm(request.POST, request.FILES, instance=user_obj)
        addform = UpdateAddressForm(request.POST, instance=user_obj)
        if userform.is_valid and addform.is_valid and profileform.is_valid:
            firstname = request.POST['first_name']
            lastname = request.POST['last_name']
            userform.save()

            addline_1 = request.POST['address_line1']
            addline_2 = request.POST['address_line2']
            phonenumber = request.POST['phone_number']
            city = request.POST['city']
            state = request.POST['state']
            country = request.POST['country']
            user_add = UserAddress.objects.create(user=request.user,address_line1=addline_1, address_line2=addline_2, phone_number=phonenumber, city=city, state=state, country=country)
            user_add.save()

            profileform.save()
            messages.success(request, 'Profile updated successfully...')
            return redirect(profile)
        else:
            messages.error(request, 'Something went wrong. Please try again later.')
            return redirect(edit_profile)
    else:
        user = request.user
        user_obj = User.objects.get(pk = user.pk)        
        userform = UpdateUserForm(instance=user_obj)
        profileform = UpdateProfileForm(instance=user_obj)
        try:
            add = UserAddress.objects.all().filter(user=user_obj).first()
            if add is not None:
                addform = UpdateAddressForm(instance=add)
            print('add = ', add)
            
            profileform = UpdateProfileForm(instance=user_obj)
           
        except Exception as e:
            print(e)
    context = {
        'user_obj' : user_obj,

        'userform': userform,
        'profileform': profileform,
        'addform': addform,
    }
    return render(request, 'account/edit_profile.html',context)


@login_required(login_url='loginuser')
def myorders(request):
    orders = Order.objects.order_by(
        'order_date').filter(user_id=request.user.id)
    order_count = orders.count()


    return render(request, 'account/my_orders.html', {
        'order_count': order_count,
        'orders': orders
    })


@login_required(login_url='loginuser')
def logout(request):
    auth_logout(request)
    request.session.flush()
    return redirect('home')



def order_success(request):


    return render(request, 'account/order_complete.html')
