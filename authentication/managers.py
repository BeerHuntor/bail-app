from django.contrib.auth.models import BaseUserManager
from authentication.utils import get_discord_profile_pic
class RegisteredUserManager(BaseUserManager):
    def create_user(self, user):

        profile_picture = self.get_discord_profile_pic(user['id'], user['avatar'])
        
        new_user = self.model(
            discord_user_id = user['id'],
            username = user['username'],
            email = user['email'],
            access_token = ['access_token'],
            refresh_token = ['refresh_token'],
            token_expiry = ['token_expiry'],
            is_police = ['is_police']        
        )

        if profile_picture:
            new_user.profile_picture.save(f'{user['id']}_{user['avatar']}.png', profile_picture)

        new_user.save(using=self._db)


    def create_super_user(self, email, username, discord_id, password=None):
        user = self.create_user(email, username, discord_id, password=None)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
