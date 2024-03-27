from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
# Register your models here.

class CustomUserAdmin(UserAdmin):

    model = User
    list_display = ('email', 'is_superuser', 'is_active', )
    list_filter = ('email', 'is_superuser', 'is_active', )
    
    fieldsets = (
        ('Authentication', {
            'fields':(
                'email', 'password',
            )
        }),            
        ('Important dates',{
            'fields':('last_login',
            )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff',
                'is_active', 'is_superuser'
            )}
        ),
    )

    search_fields = ('email', )
    ordering = ('email',)
    
        
class ProfileAdmin(admin.ModelAdmin):

    model = Profile
    list_display = ['user', 'first_name', 'last_name']


admin.site.register(User,CustomUserAdmin)
admin.site.register(Profile, ProfileAdmin)

