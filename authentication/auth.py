from django.contrib.auth.backends import BaseBackend
from authentication.models import RegisteredUser

class RegisteredUserAuthenticationBackend(BaseBackend):
    def authenticate (self, request, user) -> RegisteredUser:
        print("authenticate()")

        if user is None:
            return None

        try: 
            user_instance = RegisteredUser.objects.get(discord_user_id=user['id'])
            return user_instance
        except RegisteredUser.DoesNotExist:
            print("User was not found... Saving!")

            # Create a new user
            
        return None

    def get_user(self, user_id):
        try:
            return RegisteredUser.objects.get(pk=user_id)
        except RegisteredUser.DoesNotExist:
            return None
