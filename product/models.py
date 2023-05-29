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



class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True, null=True)
    razorpay_payment_status = models.CharField(max_length=50, blank=True, null=True)
    razorpay_payment_id = models.CharField( max_length=50, blank=True, null=True)
    paid = models.BooleanField(default=False)

    
    


STATUS_CHOICES = (
    ('PENDING', "Order Pending"),
    ('ACCEPTED', "Order Accepted"),
    ('PACKED', "YOUR ORDER IS PACKED"),
    ('ON THE WAY', "ON THE WAY TO YOUR NEAREST HUB"),
    ('DELIVERED', " ORDER IS DELEIVERED"),
    ('CANCEL ORDER', " ORDER IS CANCELLED"),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField( max_length=50, choices=STATUS_CHOICES, default='PENDING')
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, default="")

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


