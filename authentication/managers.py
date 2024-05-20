from django.contrib.auth.models import BaseUserManager
from authentication.utils import get_discord_profile_pic
class RegisteredUserManager(BaseUserManager):
    def create_user(self, user):

        profile_picture = get_discord_profile_pic(user['id'], user['avatar'])
        
        new_user = self.model(
            discord_user_id = user['id'],
            username = user['username'],
            email = user['email'],
            access_token = user['access_token'],
            refresh_token = user['refresh_token'],
            token_expiry = user['token_expiry'],
            is_police = user['is_police']        
        )

        if profile_picture:
            new_user.profile_picture.save(f'{user['id']}_{user['avatar']}.png', profile_picture)

        
        print(f"new_user.token_expiry: {new_user.token_expiry}, type: {type(new_user.token_expiry)}")

        new_user.save(using=self._db)


    def create_super_user(self, email, username, discord_id, password=None):
        user = self.create_user(email, username, discord_id, password=None)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
