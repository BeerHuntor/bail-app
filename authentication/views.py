from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from authentication.forms import LoginModalForm, UserForm, UserProfileInformation
from django.views.generic.edit import FormView

from allauth.socialaccount.models import SocialAccount
from django.conf import settings

import requests_oauthlib

GUILD_ID = '1230652347278032936'
TOKEN_ENDPOINT = 'https://discordapp.com/api/oauth2/token'

auth_redirect_url = 'https://discord.com/oauth2/authorize?client_id=1228365653254209606&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fdiscord%2Flogin%2Fcallback&scope=identify+connections+guilds.members.read+guilds'
# Create your views here.
def index_view (request): 
    form = LoginModalForm()
    return render(request, 'authentication/index.html', {'form' : form})

def login_modal (request):
    if request.method == 'POST':
        form = LoginModalForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect(reverse_lazy('authentication:index'))
            else:
                print("not a registered user")
        else:
            print("login invalid")


    else: 
        form = LoginModalForm()
    return render(request, 'authentication/login_form.html', {'form': form })

class RegisterModalView (FormView):
    user_form_class = UserForm
    profile_info_form_class = UserProfileInformation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = self.user_form_class
        context['profile_form'] = self.profile_info_form_class
        return context
    
    def form_valid(self, form):
        user = form.save

    def get_template_names(self):
        return ['authentication:register']
    
def discord_login(request):
    return redirect(auth_redirect_url)

def discord_callback(request):
    
    code = request.GET.get('code')
 # Exchange authorization code for access token
        # Make a request to Discord's token endpoint to get the access token
        # Include the necessary parameters in the request (client_id, client_secret, etc.)

        # Once you have the access token, use it to make authenticated requests to Discord's API
        # Fetch user data, including Discord ID and other relevant information

        # Example of fetching user data using requests library:
        # response = requests.get('https://discord.com/api/users/@me', headers={'Authorization': f'Bearer {access_token}'})
        # user_data = response.json()

        # Once you have the user data, create or associate a SocialAccount with the user profile
        # Example:
        # social_account = SocialAccount.objects.create(provider='discord', uid=user_data['id'], user=request.user, ...)
        
        # Display success message

    if code: 
        

        # Retrieve the access token from discord account.
        access_token = social_account.socialtoken_set.get(account=social_account).token

        # Make a request to the discord API to get the user data of a guild. 

        return redirect(reverse_lazy('authentication:index'))
    else:
        
        return HttpResponse("There was an error: Please contact the website developer stating code: <strong>DC012</strong>")

def get_discord_app_details():
    socialaccount_providers = settings.SOCIALACCOUNT_PROVIDERS

    discord_provider_settings = socialaccount_providers.get('discord, {}')

    discord_client_id = discord_provider_settings.get('APP', {}).get('client_id', '')
    discord_secret = discord_provider_settings.get('APP', {}).get('secret', '')
    discord_scope = discord_provider_settings.get('APP', {}).get('scope', [])

    return {
        'client_id' : discord_client_id,
        'secret' : discord_secret,
        'scope' : discord_scope
    }