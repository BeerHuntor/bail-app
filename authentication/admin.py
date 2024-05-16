from django.contrib import admin
from authentication.models import UserProfileInformation, UserDiscordAccountInformation
# Register your models here.
admin.site.register(UserProfileInformation)
admin.site.register(UserDiscordAccountInformation)