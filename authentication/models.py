from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInformation(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    
    def __str__ (self):
        return self.user.username
    
class UserDiscordAccountInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    discord_user_id = models.CharField(max_length=255)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
