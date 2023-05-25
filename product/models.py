from django.db import models
# from django.core.validators import RegexValidator
from django.urls import reverse
from django.conf import settings
from user.models import User, get_user_model
# Create your models here.
User = get_user_model()

class Category(models.Model):
    category_name = models.CharField(max_length=50, null=False, unique=True)
    category_image = models.ImageField(upload_to='category/', blank=True)
    slug = models.SlugField( max_length=50, unique=True,null=True)


    def __str__(self):
        return self.category_name
        
    def get_url(self):
        return reverse('products_by_category', args=[self.slug])

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'






class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=50, null=False)
    company_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, max_length=500)
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    image = models.ImageField(upload_to='images/products/',default=None)
    slug = models.SlugField(max_length=200,unique=True,null=True)
    stock = models.IntegerField(null=True)
    is_available = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    modified_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.product_name

    
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])





class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateField(auto_now_add=True)
        
    def total_cost(self):
        return self.quantity * self.product.discounted_price