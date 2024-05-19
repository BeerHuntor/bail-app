from django.contrib.auth.models import BaseUserManager

class RegisteredUserManager(BaseUserManager):
    def create_user(self, email, username, discord_id, password=None):
        if not email:
            raise ValueError("The email field must be set")
        if not username:
            raise ValueError("The username field must be set")
        if not discord_id:
            raise ValueError("The discord id field must be set")
        
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, discord_id=discord_id)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_super_user(self, email, username, discord_id, password=None):
        user = self.create_user(email, username, discord_id, password=None)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
