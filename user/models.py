from django.db import models
from . managers import CustomUserManager
from PIL import Image
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

    REQUIRED_FIELD = ['first_name', 'last_name']


    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return f'{self.email}'


class UserAddress(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    address_line1 = models.CharField(max_length=150, blank=True)
    address_line2 = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=10)
    city = models.CharField(max_length=30, null=True)
    state = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=40, null=True)

    def __str__(self):
        return f'{self.user}'

    def full_address(self):
        return f'{self.address_line1} + " " +  {self.address_line2}'

    
class Profile(models.Model):

    user = models.OneToOneField(User, verbose_name=("Customer"), on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='images/userprofile')

    def __str__(self):
        return f"{self.user.email}"

  


    def save(self):
        super().save()

        img = Image.open(self.profile_image.path)

        if img.height > 85 or img.width > 85:
            output_size = (85,85)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)


