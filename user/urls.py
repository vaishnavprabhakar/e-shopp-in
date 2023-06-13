from django.urls import path
from django.contrib import admin
from . import views
from .forms import MyPasswordChange, MySetPasswordForm, MyPasswordResetForm
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	path('',views.home,name='home'),
    path('sign/',views.sign,name='signup'),
    path('login/',views.loginuser, name='loginuser'),
    
    path('logout/',views.logout, name='logout'),
    path('active/<slug:uidb64>/<slug:token>/',views.active, name='active'),


    path("password_change/", auth_views.PasswordChangeView.as_view(template_name='account/password_change.html'),name='password_change'),
    path("password_change_done/", auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'),name='password_change_done'),

    path("password_reset/", auth_views.PasswordResetView.as_view(template_name='account/password_reset.html',form_class=MyPasswordResetForm) ,name='reset_password'),
    path("password_reset_done/", auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),name='password_reset_done'),
    path("password_reset_confirm/<slug:uidb64>/<slug:token>/", auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html',form_class=MySetPasswordForm), name="password_reset_confirm"),
    path("password_reset_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),name='password_reset_complete'),


	path('profile/',views.profile,name='profile'),
	path('edit_profile/',views.edit_profile,name='edit_profile'),
    
	path('orders/',views.myorders,name='my_orders'),
    path('order_success/', views.order_success,name='order_success'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)