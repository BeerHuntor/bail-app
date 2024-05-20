from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from authentication.forms import LoginModalForm, UserRegisterModalForm
from authentication.utils import calculate_token_expiry, exchange_code_for_token_data, get_user_data_from_discord, is_police

import requests


GUILD_ID = '1230652347278032936'
TEST_GUILD_ID = '891382242729939014' # Returns code 10004 when not a member and null json. 
TOKEN_ENDPOINT = 'https://discordapp.com/api/oauth2/token'

REGISTER_AUTH_REDIRECT_URI = 'https://discord.com/oauth2/authorize?client_id=1228365653254209606&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Fregister%2Fcallback&scope=identify+connections+guilds.members.read+guilds+email'
LOGIN_AUTH_REDIRECT_URI = 'https://discord.com/oauth2/authorize?client_id=1228365653254209606&response_type=code&redirect_uri=http%3A%2F%2F127.0.0.1%3A8000%2Flogin%2Fcallback&scope=identify+connections+guilds.members.read+guilds+email'
# Create your views here.
"""
# region Views
"""
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

# User gets directed to the discord auth page then gets taken to the callback
def discord_login(request):
    return redirect(LOGIN_AUTH_REDIRECT_URI)

#This is where the user is redirected after a successful auth. 
def discord_login_callback(request):
    return JsonResponse ({'msg' : 'Discord Login'})

# User gets directed to the discord auth page then gets taken to the callback    
def discord_register(request):
    return redirect(REGISTER_AUTH_REDIRECT_URI)

#This is where the user is redirected after a successful auth. 
def discord_register_callback(request):
    redirect_uri = request.build_absolute_uri('/register/callback') # This is the redirect url where we are redirected to upon authentication including the ?code
    code = request.GET.get('code')

    if code:
        # Exchange for token data
        token_data = exchange_code_for_token_data(code=code, redirect_uri=redirect_uri)
        if token_data: 
            access_token = token_data['access_token']
            token_expiry_time = calculate_token_expiry(token_data['expires_in'])
            refresh_token = token_data['refresh_token']
            # Request discord API for user object
            user_data = get_user_data_from_discord(token=access_token)
            user_data['access_token'] = access_token
            user_data['token_expiry'] = token_expiry_time
            user_data['refresh_token'] = refresh_token
            #user_data['is_police'] = is_police(user_data=user_data)
        else:
            print("No access token found.")
    else:
        print("No code found.")        
    
    return JsonResponse ({'msg' : 'Discord Registration'})

"""
# endregion
"""