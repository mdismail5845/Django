from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from account.models import User

# Register your models here.
@admin.register(User)
class UserModelAdmin(UserAdmin):
    model = User
    list_display = [
        'id','email','name','city','is_active','is_staff','is_superuser','is_customer','is_seller','created_at','updated_at'
    ]
    list_filter = [ 'is_superuser' ]

    search_fields = ['email']
    ordering =['email','id']
    filter_horizontal = []

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','city')}),
        ('Permissions', {'fields': ('is_active','is_staff','is_superuser','is_customer','is_seller','groups','user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','password1','password2','is_active','is_staff','is_superuser','is_customer','is_seller'),
        }),
    )