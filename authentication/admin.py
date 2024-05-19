from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from authentication.models import RegisteredUser
# Register your models here.

class UserAdmin(BaseUserAdmin):
    model = RegisteredUser
    list_display = ('username', 'email', 'discord_user_id','is_staff','is_active', 'date_registered')
    list_filter = ('is_staff', 'is_active', 'is_police')
    fieldsets = (
        (None, {'fields': ('discord_user_ud', 'username','email', 'password')}),
        (_('Personal info'), {'fields': ('profile_picture', 'access_token', 'refresh_token', 'token_expiry', 'last_login')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_police', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('date_regsistered',)}),
    )

    add_fieldsets = (
        (None, {
            'classes' : ('wide',),
            'fields' : ('discord_user_id', 'username', 'email', 'password1', 'password2', 'is_staff', 'is_active', 'is_police', 'groups')}

        ),
    )

    search_fields = ('username', 'email', 'discord_user_id')
    ordering = ('username',)
admin.site.register(RegisteredUser)