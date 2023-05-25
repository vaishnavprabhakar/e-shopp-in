from django.contrib import admin
from .models import User,UserAddress
from django.contrib.auth.admin import UserAdmin
# from admin_thumbnails import thumbnail

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','first_name','last_name','last_login', 'is_active','is_email_verified')
    list_display_links = ('email','first_name','last_name')
    readonly_fields = ('last_login',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()
    ordering = ('first_name','-id')
admin.site.register(User,UserAdmin)

   
admin.site.register(UserAddress)
