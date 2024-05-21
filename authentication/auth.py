from django.contrib.auth.backends import BaseBackend
from authentication.models import RegisteredUser

class RegisteredUserAuthenticationBackend(BaseBackend):
    def authenticate (self, request, user) -> RegisteredUser:

        if user is None:
            return None

        try: 
            existing_user = RegisteredUser.objects.get(discord_user_id=user['id'])
            existing_user.access_token = user['access_token']
            existing_user.token_expiry = user['token_expiry']
            existing_user.refresh_token = user['refresh_token']

            existing_user.save()
            return existing_user
            
        except RegisteredUser.DoesNotExist:
            print("User was not found... Saving!")

            # Create a new user
            new_user = RegisteredUser.objects.create_user(user)
            return new_user      

    def get_user(self, user_id):
        try:
            return RegisteredUser.objects.get(pk=user_id)
        except RegisteredUser.DoesNotExist:
            return None
