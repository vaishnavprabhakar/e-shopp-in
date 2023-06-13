from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from .models import User
from django.core import validators
from django.contrib.auth import get_user_model
from .models import UserAddress, Profile
from django.forms import ModelForm
# from phonenumber_field.modelfields import PhoneNumber
# from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
# from captcha.fields import ReCaptchaField

User = get_user_model()




class UpdateAddressForm(forms.ModelForm):
    address_line1 = forms.CharField(max_length=256,
                                 required=True,
                                 label='address_line1',
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'name': 'address_line1',
                                         'autofocus': True,
                                         'placeholder': 'address_line1'
                                     }))
    address_line2 = forms.CharField(max_length=256,
                                 required=True,
                                 label='address_line2',
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'name': 'address_line2',
                                         'autofocus': True,
                                         'placeholder': 'address_line2'
                                     }))

    phone_number = forms.CharField( required=True, widget=forms.NumberInput(
                                        attrs={
                                         'class' :'form-control',
                                         'name': 'phone_number',
                                         'autofocus': True,
                                         'placeholder': 'Phone Number'
                                        }))


    city = forms.CharField(max_length=20,
                                 required=True,
                                 label='city',
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'name': 'city',
                                         'autofocus': True,
                                         'placeholder': 'city'
                                     }))
    state = forms.CharField(max_length=20,
                                 required=True,
                                 label='state',
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'name': 'state',
                                         'autofocus': True,
                                         'placeholder': 'state'
                                     }))


    country = forms.CharField(max_length=20,
                                 required=True,
                                 label='country',
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                
                                         'name': 'country',
                                         'autofocus': True,
                                         'placeholder': 'country'
                                     }))
    class Meta:
        model = UserAddress
        fields = ('address_line1','address_line2','phone_number','city','state', 'country',)


class UpdateProfileForm(forms.ModelForm):
     profile_image = forms.ImageField(
                                 required=False,
                                 label='Profile image',help_text='Optional input for the profile image', widget=forms.FileInput())
     class Meta:
        model = Profile
        fields = ("profile_image",)


class UpdateUserForm(forms.ModelForm):
     first_name = forms.CharField(max_length=20,
                                 required=True,
                                 label='First name',
                                 validators=[validators.MinLengthValidator(4)],
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'name': 'first_name',
                                         'autofocus': True,
                                         'placeholder': 'First Name'
                                     }))

     last_name = forms.CharField(max_length=20,
                                 required=True,
                                 label='Lastname',
                                 validators=[validators.MinLengthValidator(4)],
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'name': 'last_name',
                                         'autofocus': True,
                                         'placeholder': 'First Name'
                                     }))
    
     class Meta:
        model = User
        fields = ('first_name', 'last_name',)



# End of the form ========================



class UserForm(UserCreationForm):

    User = get_user_model()
    first_name = forms.CharField(max_length=20,
                                 required=True,
                                 label='Firstname',
                                 validators=[validators.MinLengthValidator(4)],
                                 widget=forms.TextInput(
                                     attrs={
                                         'class': 'form-control',
                                         'name': 'first_name',
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
                             #validators=[validators.validate_email],
                             widget=forms.TextInput(
                                 attrs={
                                     'class': 'form-control',
                                     'autofocus': True,
                                     'placeholder': 'Enter Email',
                                     'name': 'email'
                                 }))

    password1 = forms.CharField(required=True,
                                label='Password',
                                help_text="Password requires atleast one capital letter, numerics and special charectors",
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



class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={
                                 'class': 'form-control col-md-6',
                                 'name': 'email'
                             }))

class MySetPasswordForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control col-md '}))
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control col-md'}))

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

