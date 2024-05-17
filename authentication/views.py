from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from authentication.forms import LoginModalForm, UserRegisterModalForm
from django.views.generic.edit import FormView
from authentication.models import UserDiscordAccountInformation

from django.conf import settings
from allauth.socialaccount.models import SocialAccount
import requests
from datetime import timedelta, datetime

import json

GUILD_ID = '1230652347278032936'
TEST_GUILD_ID = '891382242729939014' # Returns code 10004 when not a member and null json. 
TOKEN_ENDPOINT = 'https://discordapp.com/api/oauth2/token'

REGISTER_AUTH_REDIRECT_URI = 'https://discord.com/oauth2/authorize?client_id=1228365653254209606&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fdiscord%2Fregister%2Fcallback&scope=identify+connections+guilds.members.read+email'
LOGIN_AUTH_REDIRECT_URI = 'https://discord.com/oauth2/authorize?client_id=1228365653254209606&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fdiscord%2Flogin%2Fcallback&scope=identify+connections+guilds.members.read+guilds'
LINK_AUTH_REDIRECT_URI = 'https://discord.com/oauth2/authorize?client_id=1228365653254209606&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Faccounts%2Fdiscord%2Flink%2Fcallback&scope=identify+connections+guilds.members.read+email'
# Create your views here.

def index_view (request): 
    form = LoginModalForm()
    register_form = UserRegisterModalForm()
    return render(request, 'authentication/index.html', {'form' : form, 'register_form' : register_form})

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

class UserRegisterModalView(FormView):
    template_name = 'authentication/index.html'
    form_class = UserRegisterModalForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'register_form' not in context:
            context['register_form'] = self.form_class()
        return context
    
    def form_valid(self, form):
        user = form.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def form_invalid(self, form):
        print("Form Data: ", self.request.POST)
        print("Form errors: ", form.errors)
        return self.render_to_response(self.get_context_data(register_form=form))

    def get_success_url(self):
        return reverse('authentication:index') + '?modal=success'

    
def discord_register(request):
    return redirect(REGISTER_AUTH_REDIRECT_URI)

def discord_register_callback(request):
    pass

def discord_login(request):
    return redirect(LOGIN_AUTH_REDIRECT_URI)

def discord_login_callback(request):
    pass

def discord_link(request):
    return redirect(LINK_AUTH_REDIRECT_URI)

def discord_link_callback(request):
    redirect_uri = request.build_absolute_uri('/accounts/discord/link/callback')
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

            access_token = response_data.get('access_token', '')
            token_expiry = calculate_token_expiry(response_data.get('expires_in', ''))
            discord_user_id = get_user_data_from_discord(access_token).get('id', '')

            link_discord_account(request.user, discord_user_id, response_data.get('access_token', ''),  response_data.get('refresh_token', ''), token_expiry)


            #print(get_user_discord_account_information(request.user))

        else:
            # Request Failed
            print('Error:', response.status_code, response.text)
        return redirect(reverse_lazy('authentication:index'))
    else:
        return HttpResponse("There was an error: Please contact the website developer stating code: <strong>DC012</strong>")

# Gets details of the discord app
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

# Gets discord user data - top level
def get_user_data_from_discord(token):
    # User Data End Point URI
    user_data_endpoint = 'https://discord.com/api/users/@me'

    headers = { 
        'Authorization' : f'Bearer {token}'
    }
    request_data = get_request_discord_api_json(user_data_endpoint, headers)
    if request_data:
        #We have something
        return request_data
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

# Gets user model from PD discord guild. 
def get_user_guild(token):
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

# Gets user roles for guild
def get_user_guild_roles(data):
    role_ids = data.get('roles', {})
    return role_ids

def link_discord_account(user, discord_user_id, access_token, refresh_token, token_expiry):
    user_discord_account_information = UserDiscordAccountInformation.objects.create(
        user=user,
        discord_user_id = discord_user_id,
        access_token = access_token,
        refresh_token = refresh_token,
        token_expiry = token_expiry,
    )

    return user_discord_account_information

def get_user_discord_account_information(user):
    try:
        return UserDiscordAccountInformation.objects.get(user=user)
    except UserDiscordAccountInformation.DoesNotExist:
        return None

def get_role_name_by_id (role_id, guild_roles):
    for role in guild_roles:
        if role['id'] == role_id:
            return role['name']
    return None

def get_request_discord_api_json(endpoint, headers):

    response = requests.get(endpoint, headers=headers)

    if response.status_code == 200:
        # We have a response
        return response.json()
    else: 
        print('ERROR: ', response.status_code, response.text)

def calculate_token_expiry(expires_in):
    current_time = datetime.now()

    duration = timedelta(seconds=expires_in)

    return current_time + duration