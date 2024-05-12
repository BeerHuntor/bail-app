from authentication.models import UserProfileInformation

# Context processors allow context to be sent with any request automatically,  so this instance is getting the UserProfielInformation model and passing it to every request to 
# enable access for every template by default. 
def user(request):
    user_profile = None
    
    if request.user.is_authenticated:
        user_profile = UserProfileInformation.objects.get_or_create(user=request.user)[0]
    return { 'user_profile' : user_profile }