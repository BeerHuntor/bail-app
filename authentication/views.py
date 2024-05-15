from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login
from authentication.forms import LoginModalForm, UserForm, UserProfileInformation
from django.views.generic.edit import FormView

from django.conf import settings
from allauth.socialaccount.models import SocialAccount
import requests

import json

GUILD_ID = '1230652347278032936'
TEST_GUILD_ID = '891382242729939014' # Returns code 10004 when not a member and null json. 
TOKEN_ENDPOINT = 'https://discordapp.com/api/oauth2/token'
ACCESS_TOKEN = ''

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
    redirect_uri = request.build_absolute_uri('/accounts/discord/login/callback')
    code = request.GET.get('code')

    if code: 
        discord_details = get_discord_app_details()
        # Request Access Token
        payload = {
            'client_id' : discord_details.get('client_id', ''),
            'client_secret' : discord_details.get('secret', ''),
            'grant_type' : 'authorization_code',
            'code' : code, 
            'redirect_uri' : redirect_uri,
            'scope' : discord_details.get('scope', '')
        }

        response = requests.post(TOKEN_ENDPOINT, data=payload)

        if response.status_code == 200:
            # Process the response data
            response_data = response.json()
            global ACCESS_TOKEN
            ACCESS_TOKEN = response_data.get('access_token', '')
            get_user_data_from_discord(ACCESS_TOKEN)
        else:
            # Request Failed
            print('Error:', response.status_code, response.text)
        return redirect(reverse_lazy('authentication:index'))
    else:
        
        return HttpResponse("There was an error: Please contact the website developer stating code: <strong>DC012</strong>")

def get_discord_app_details():
    socialaccount_providers = settings.SOCIALACCOUNT_PROVIDERS

    discord_provider_settings = socialaccount_providers.get('discord', {})

    discord_client_id = discord_provider_settings.get('APP', {}).get('client_id', '')
    discord_secret = discord_provider_settings.get('APP', {}).get('secret', '')
    discord_scope = discord_provider_settings.get('APP', {}).get('scope', [])

    return {
        'client_id' : discord_client_id,
        'secret' : discord_secret,
        'scope' : discord_scope
    }

def get_user_data_from_discord(token):
    # User Data End Point URI
    user_data_endpoint = 'https://discord.com/api/users/@me'

    headers = { 
        'Authorization' : f'Bearer {token}'
    }
    request_data = get_request_discord_api_json(user_data_endpoint, headers)
    if request_data:
        #We have something
        pass
    else:
        print("No User JSON object recieved or returned an error.")

# NOT USED - USED FOR DEBUG
def get_user_guilds_info(token):
    #  Guilds endpoint
    guild_endpoint = 'https://discord.com/api/users/@me/guilds'

    headers = {
        'Authorization' : f'Bearer {token}'
    }

    request_data = get_request_discord_api_json(guild_endpoint, headers)

    if request_data:
        return request_data
    else: 
        print('No Guilds JSON object recieved or returned an error.')

def check_if_discord_guild_member(token):
    # Guild Information
    guild_member_endpoint = f'https://discord.com/api/users/@me/guilds/{GUILD_ID}/member'
    
    headers = {
        'Authorization' : f'Bearer {token}'
    }

    request_data = get_request_discord_api_json(guild_member_endpoint, headers)
    if request_data: 
        # We have something
        return request_data
    else :
        print ("No Guild JSON data received or returned an error.")

def get_request_discord_api_json(endpoint, headers):

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        # We have a response
        return response.json()
    else: 
        print('ERROR: ', response.status_code, response.text)    

