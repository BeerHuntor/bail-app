from django.conf import settings
from authentication.models import RegisteredUser

# Context processors allow context to be sent with any request automatically,  so this instance is getting the UserProfielInformation model and passing it to every request to 
# enable access for every template by default. 

def user_profile(request):
    user_profile = None
    
    if request.user.is_authenticated:
        if isinstance(request.user, RegisteredUser):
            try:
                user_profile = RegisteredUser.objects.get(discord_user_id=request.user.discord_user_id)
            except RegisteredUser.DoesNotExist:
                user_profile = None
    return { 'user_profile' : user_profile }