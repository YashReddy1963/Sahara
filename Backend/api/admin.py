from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username', 'otp_verified', 'is_staff', 'is_active')  # Added 'is_staff' and 'is_active'
    list_filter = ('otp_verified', 'is_staff', 'is_active')

    fieldsets = (
    (None, {'fields': ('email', 'username', 'password')}),
    ('Personal Info', {'fields': ('contact_number', 'profile_picture')}),
    ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),  
    ('OTP Verification', {'fields': ('otp_verified', 'otp_code')}),
)



    search_fields = ('email', 'username')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
