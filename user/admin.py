from django.contrib import admin
from .models import User,UserAddress, Profile
from django.contrib.auth.admin import UserAdmin
# from admin_thumbnails import thumbnail
from django.utils.html import format_html


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




@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;>'.format(object.profile_image.url))

    list_display =['user','thumbnail'] 
    thumbnail.short_description = 'Profile Picture' 
    list_display_links = ['thumbnail', 'user']