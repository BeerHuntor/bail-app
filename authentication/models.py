from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInformation(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)

    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    
    def __str__ (self):
        return self.user.username
    
class UserDiscordAccountInformation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    discord_user_id = models.CharField(max_length=255, null=True)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_expiry = models.DateTimeField(auto_now=False, auto_now_add=False)

    def save(self,*args, **kwargs):
        if not self.token_expiry.tzinfo:
          # Make the token_expiry datetime aware using the current timezone
            self.token_expiry = timezone.make_aware(self.token_expiry, timezone.get_current_timezone())
        super().save(*args, **kwargs)