from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from authentication.managers import RegisteredUserManager

# Create your models here.
   
class RegisteredUser(AbstractBaseUser, PermissionsMixin):
    objects = RegisteredUserManager()

    discord_user_id = models.CharField(primary_key=True, max_length=255, unique=True)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    token_expiry = models.DateTimeField(auto_now=False, auto_now_add=False)
    last_login = models.DateTimeField(auto_now=True, auto_now_add=False)
    date_registered = models.DateTimeField(auto_now=False, auto_now_add=True)
    profile_picture = models.ImageField(upload_to='media/profile_pics/', height_field=None, width_field=None, max_length=None)
    is_police = models.BooleanField(default=False)


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['username', 'discord_id']

    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='registereduser_set', #Changed related name to avoid clash, 
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='registereduser_set', # Changed related name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def save(self, *args, **kwargs):
        if self.token_expiry is not None and not self.token_expiry.tzinfo:
            self.token_expiry = timezone.make_aware(self.token_expiry, timezone.get_current_timezone())
        if self.last_login is None or not self.last_login.tzinfo:
            self.last_login = timezone.now()
        if self.date_registered is None or not self.date_registered.tzinfo:
            self.date_registered = timezone.now()

        print(f"token_expiry: {self.token_expiry}, type: {type(self.token_expiry)}")
        print(f"last_login: {self.last_login}, type: {type(self.last_login)}")
        print(f"date_registered: {self.date_registered}, type: {type(self.date_registered)}")
        super().save(*args, **kwargs)


    def is_authenticated(self, request):
        return True
    
    def __str__(self):
        return self.username