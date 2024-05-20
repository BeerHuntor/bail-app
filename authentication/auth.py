from django.contrib.auth.backends import BaseBackend
from authentication.models import RegisteredUser

class RegisteredUserAuthenticationBackend(BaseBackend):
    def authenticate (self, request, user) -> RegisteredUser:

        if user is None:
            return None

        try: 
            existing_user = RegisteredUser.objects.get(discord_user_id=user['id'])
            print(f"Existing User: {existing_user}")
            return existing_user
        except RegisteredUser.DoesNotExist:
            print("User was not found... Saving!")

            # Create a new user
            new_user = RegisteredUser.objects.create_user(user)
            print(new_user)
            return new_user
            
        

    def get_user(self, user_id):
        try:
            return RegisteredUser.objects.get(pk=user_id)
        except RegisteredUser.DoesNotExist:
            return None
