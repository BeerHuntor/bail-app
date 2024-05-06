from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfileInformation(models.Model):

    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)

    display_name = models.CharField(max_length=50, null=True)
    is_police = models.BooleanField(default=False)
    profile_picture = models.ImageField(upload_to='profile_pics', blank=True)
    
    def __str__ (self):
        return self.user.username