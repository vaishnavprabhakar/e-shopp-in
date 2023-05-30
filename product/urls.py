from django.urls import path
from . import views
from django.contrib import admin
# from django.contrib.auth import views


# Your urlpatterns will be here...

urlpatterns = [
    path('home/', views.homepage, name='home'),

    # path("show-address/", views.address_show, name='address'),
    
    # path("address-show/",views.address_show, name='profile-show'),

    
    # path("<slug:category_slug>/", views.product_detail, name='product_detail'),
    
    path("<slug:category_slug>/<slug:product_slug>/", views.product_detail, name='product_detail'),
    
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'), 
    
    path('cartsd/', views.carth, name='cart'), 
    

    path('pluscart/', views.pluscart),            
    path('minuscart/', views.minuscart),            
    path('removecart/', views.removecart),            

    path('checkout/', views.checkout, name='checkout'),            
    path('paymentdone/', views.paymentdone, name='paymentdone'),            
    path('orders/', views.homepage, name='orders'),            
    
    
    path("<slug:category_slug>/", views.homepage, name='products_by_category'),

    # path('wishlist/', views.add_to_wishlist, name='wishlist'),
]


admin.site.site_header  =  "Mrz  Shoppie"
admin.site.site_title = "Mrz Shoppie"
admin.site.index_title = "Welcome to Mrz Shoppie"