from django.conf import settings
from authentication.models import RegisteredUser

# Context processors allow context to be sent with any request automatically,  so this instance is getting the UserProfielInformation model and passing it to every request to 
# enable access for every template by default. 

def user_profile(request):
    registered_user = None
    
    if request.user.is_authenticated:
        if isinstance(request.user, RegisteredUser):
            try:
                registered_user = RegisteredUser.objects.get(discord_user_id=request.user.discord_user_id)
                registered_user.is_authenticated = True
            except RegisteredUser.DoesNotExist:
                registered_user = None
    return { 'registered_user' : registered_user }