from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User



class MyUserAdmin(UserAdmin):
    list_display = ['email', 'first_name']
    search_fields = ['email', 'first_name']
    ordering = ['email']
    fieldsets = (
        ('Personal information', {
            'fields': ('email', 'password', 'first_name', 'last_name')
        }),
        ('Date information', {
            'fields': ('date_joined', 'last_login')
        }),
        ('Other information', {
            'fields': ('is_staff', 'is_active', 'is_superuser'
                       )
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )


admin.site.register(User, MyUserAdmin)
