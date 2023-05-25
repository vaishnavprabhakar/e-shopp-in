from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import User
from django.core import validators
from django.contrib.auth import get_user_model
from .models import UserAddress
from django.forms import ModelForm
# from phonenumber_field.modelfields import PhoneNumber
# from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
# from captcha.fields import ReCaptchaField

User = get_user_model()




class UserForm(UserCreationForm):
    User = get_user_model()
    first_name = forms.CharField(max_length=20,
                                 required=True,
                                 label='Firstname',
                                 validators=[validators.MinLengthValidator(4)],
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'name': 'firstname',
                                         'autofocus': True,
                                         'placeholder': 'First Name'
                                     }))

    last_name = forms.CharField(
        max_length=20,
        required=True,
        label='Lastname',
        validators=[validators.MinLengthValidator(1)],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'name': 'lastname',
            'placeholder': 'Lastname'
        }))

    email = forms.EmailField(
        required=True,
        max_length=100,
        label='Email',
        validators=[
            validators.MinLengthValidator(4),
            validators.EmailValidator()
        ],
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email',
            'name': 'email'
        }))

    password1 = forms.CharField(
        max_length=50,
        required=True,
        label='Password',
        validators=[
            validators.MinLengthValidator(6),
            validators.MaxLengthValidator(16)
        ],
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'name': 'passowrd',
            'placeholder': 'Password'
        }))

    password2 = forms.CharField(max_length=50,
                                required=True,
                                label='Re-Password',
                                validators=[
                                    validators.MinLengthValidator(6),
                                    validators.MaxLengthValidator(16)
                                ],
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'name': 'password2',
                                        'placeholder': 'Repeat Password'
                                    }))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # del self.fields['username']

    class Meta:

        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    User = get_user_model()
    email = forms.EmailField(required=True,
                             max_length=100,
                             label='Email',
                             validators=[validators.validate_email],
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'autofocus': True,
                                     'placeholder': 'Enter Email',
                                     'name': 'email'
                                 }))

    password1 = forms.CharField(required=True,
                                label='Password',
                                validators=[validators.MinLengthValidator(8)],
                                widget=forms.PasswordInput(
                                    attrs={
                                        'class': 'form-control',
                                        'name': 'password1',
                                        'placeholder': 'Password'
                                    }))

    class Meta:
        model = get_user_model()
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'], self.fields['password1']
        del self.fields['username'], self.fields['password']


class AddressForm(forms.ModelForm):

    #  email = forms.EmailField(required=True,
    #                          max_length=100,
    #                          label='Email',
    #                          validators=[validators.validate_email],
    #                          widget=forms.TextInput(
    #                              attrs={
    #                                  'class': 'form-group',
    #                                  'autofocus': True,
    #                                  'placeholder': 'Enter Email',
    #                                  'name': 'email'
    #                              }))

    profile = forms.ImageField(label='', required=False)  #profile

    phone_number = forms.CharField(
        label='',
        max_length=12,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control pt-3',
                'placeholder': 'Enter Phone',  # phone_number
                'name': 'phone_number'
            }))


    place = forms.CharField(
        max_length=30,
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-3',  # place
                'placeholder': 'Place',
                'name': 'place'
            }))

    landmark = forms.CharField(
        label='',
        max_length=40,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',  #landmark
                'placeholder': 'Enter Landmark',
                'name': 'landmark'
            }))

            
    city = forms.CharField(
        max_length=30,
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',  # city
                'placeholder': 'City',
                'name': 'city'
            }))

    zipcode = forms.IntegerField(
        label='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',  # zipcode
                'placeholder': 'Enter zipcode',
                'name': 'zipcode'
            }))

    district = forms.CharField(
        max_length=30,
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Enter district',  #district
                'name': 'district'
            }))

    country = forms.CharField(
        max_length=30,
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control mt-2',
                'placeholder': 'Enter country',  # country
                'name': 'country'
            }))

    class Meta:
        model = UserAddress
        fields = ('profile', 'phone_number', 'landmark', 'place', 'city',
                  'zipcode', 'district', 'country')


# Password Reset Form
class MyPasswordResetForm(PasswordResetForm):

    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control col-md-6',
                                 'name': 'email'
                             }))





class MySetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-group'}))
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-group'}))


class MyPasswordChange(PasswordChangeForm):
    
    old_password = forms.CharField(label='Old Password',
                                   widget=forms.PasswordInput(
                                       attrs={
                                           'autofocus': 'True',
                                           'autocomplete': 'Current Password',
                                           'class': 'form-group'
                                       }))

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'Current Password',
            'class': 'form-group'
        }))
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'autocomplete': 'Current Password',
            'class': 'form-group'
        }))



