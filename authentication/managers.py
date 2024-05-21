from django.contrib.auth.models import BaseUserManager
from django.core.files import File
from authentication.utils import get_discord_profile_pic

import os

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

        """
        # In theory an already existing profile picture, can't exist unless the user deletes their account, and re registers at a later date.
        # Possible cause for problems as we currently don't deal with removing profile images at account deletion.
        """
        if profile_picture:
            file_name = f'{user['id']}_{user['avatar']}.png'
            directory = 'media/profile_pics'
            file_path = os.path.join(directory, file_name)

            if not os.path.exists(file_path):
                new_user.profile_picture.save(f'{user['id']}_{user['avatar']}.png', profile_picture)

            else:
                print("Profile Picture already exists within the db")

        
        print(f"new_user.token_expiry: {new_user.token_expiry}, type: {type(new_user.token_expiry)}")

        new_user.save(using=self._db)


    def create_super_user(self, email, username, discord_id, password=None):
        user = self.create_user(email, username, discord_id, password=None)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
