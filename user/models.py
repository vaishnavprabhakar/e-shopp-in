from django.db import models
from . managers import CustomUserManager

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
# from thumbnail import thumbnail
from django.utils.html import mark_safe
from django.core.validators import RegexValidator
from django.conf import settings
import uuid
from django.conf import settings
# Create your models here.




# +++++++++++++++++++++++++++++++++++++


emailvalidation = RegexValidator(
    r'^[a-z0-9@gmail.com]*$',
    'Email contains meaningfull alphanumeric charector only')
alphanumeric = RegexValidator(r'^[a-zA-Z]*$',
                              'Only alphanumeric characters are allowed.')




# <!======================= Custom user mode===============

class User(AbstractBaseUser, PermissionsMixin):

    
    email = models.EmailField(max_length=60,
                              null=False,
                              unique=True,
                              validators=[emailvalidation])
    first_name = models.CharField(max_length=20, validators=[alphanumeric])
    last_name = models.CharField(max_length=20, validators=[alphanumeric])

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    # EMAIL_FIELD = 'email'
    REQUIRED_FIELD = ['first_name', 'last_name']

    list_display = [
        'email', 'first_name', 'last_login', 'is_superuser', 'is_staff',
        'is_active'
    ]

    readonly_fields = ['__all__']

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return f'{self.email}\'s Profile'


class UserAddress(models.Model):

    
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    profile = models.ImageField(upload_to='images/userprofile/', null=True)
    phone_number = models.CharField(max_length=13, unique=True)
    landmark = models.CharField(max_length=30, null=True)
    place = models.CharField(max_length=30, null=True)
    city = models.CharField(max_length=30, null=True)
    district = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=40, null=True)
    zipcode = models.IntegerField(verbose_name='PIN')

    def __str__(self):
        return f'{self.user }\'s Address'