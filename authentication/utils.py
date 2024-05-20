import requests
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from datetime import datetime, timedelta

from django.conf import settings

class CustomErrorResponse:
    def __init__(self, success, data=None, error_message=None):
        self.success = success
        self.data = data
        self.error_message = error_message

# Discord API Function
def get_request_discord_api_json(endpoint, headers):
    discord_api_url = 'https://discord.app.com/api'
    response = requests.get(f'{discord_api_url}{endpoint}', headers=headers)

    if response.status_code == 200:
        # We have a response
        return response.json()
    else: 
        error_message = f'Error: {response.status_code}, {response.text}'
        return CustomErrorResponse(success=False, error_message=error_message)

# Time and Date utility
def calculate_token_expiry(expires_in):
    current_time = datetime.now()

    duration = timedelta(seconds=expires_in)

    return current_time + duration

# Returns discord profile picture
def get_discord_profile_pic(discord_id, avatar):
    profile_pic_url = f'https://cdn.discordapp.com/avatars/{discord_id}/{avatar}.png'
    response = requests.get(profile_pic_url)

    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img_io = BytesIO()
        img.save(img_io, format='PNG')
        img_content = ContentFile(img_io.getvalue(), f'{discord_id}_{avatar}.png')
        return img_content
    else:
        error_message = f'Failed to retrieve profile picutre for {discord_id}.'
        return CustomErrorResponse(success=False, error_message=error_message)

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

"""
# region discord API Calls
"""
# Exchanges code for access_token, refresh_token and token expiry
def exchange_code_for_token_data(code, redirect_uri):
    token_endpoint = f'{DISCORD_API_URL}/oauth2/token'
    
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

        response = requests.post(token_endpoint, data=payload)

        if response.status_code == 200:
            # Process the response data
            response_data = response.json()
            token_data = {
                'access_token' : response_data.get('access_token', ''), 
                'expires_in' : response_data.get('expires_in', ''), 
                'refresh_token' : response_data.get('refresh_token', ''),
            }
            print(token_data)
            
            return token_data

        else:
            error_message = f'Error: No Access Token found: {response.status_code}, {response.text}'
            # Request Failed
            return CustomErrorResponse(success=False, error_message=error_message)
    else:
        error_message = "Error: No Code Provided"
        return CustomErrorResponse(success=False, error_message=error_message)

# Gets discord account information as user data - top level
def get_user_data_from_discord(token):
    # User Data End Point URI
    user_data_endpoint = '/users/@me'

    headers = { 
        'Authorization' : f'Bearer {token}'
    }
    request_data = get_request_discord_api_json(user_data_endpoint, headers)
    if request_data:
        #We have something
        return request_data
    else:
        error_message = 'User JSON could not be retrieved'
        return CustomErrorResponse(success=False, error_message=error_message)

# Gets user object from PD discord guild. 
def get_user_guild(token):
    guild_id = '1230652347278032936'
    # Guild Information
    guild_member_endpoint = '/users/@me/guilds/{guild_id}/member'
    
    headers = {
        'Authorization' : f'Bearer {token}'
    }

    request_data = get_request_discord_api_json(guild_member_endpoint, headers)
    if request_data: 
        # We have something
        return request_data
    else :
        error_message = "User guild JSON could not be retrieved."
        return CustomErrorResponse(success=False, error_message=error_message)
 
def get_guild_roles(guild_id, bot_token):
    pass

# NOT USED - USED FOR DEBUG
def get_all_users_guilds(token):
    #  Guilds endpoint
    guild_endpoint = '/users/@me/guilds'

    headers = {
        'Authorization' : f'Bearer {token}'
    }

    request_data = get_request_discord_api_json(guild_endpoint, headers)

    if request_data:
        return request_data
    else: 
        error_message = 'No User JSON found!'
        return CustomErrorResponse(success=False, error_message=error_message)

"""
# endregion
"""

"""
# region Helper Functions
"""
# Check if is police in the correct discord
def is_police(user_data):
    ROLE_ID = 1230652347307393087 # NEERP Police Role

    guild_data = get_user_guild(user_data['access_token'])
    if guild_data:
        #They are a member of PD discord
        guild_roles = get_user_guild_roles(guild_data)
        get_role_name_by_id(ROLE_ID, guild_roles=guild_roles)

# Gets user roles for guild
def get_user_guild_roles(user_data):
    role_ids = user_data.get('roles', {})
    return role_ids

# checks the database for the registered user if it exists, and returns none if doesn't
def get_registereduser_if_exist(user):
    from authentication.models import RegisteredUser # Dynamic import to avoid circular import issues
    try:
        return RegisteredUser.objects.get(user=user)
    except RegisteredUser.DoesNotExist:
        return None
    
def get_role_name_by_id (role_id, guild_roles):
    for role in guild_roles:
        if role['id'] == str(role_id):
            print(role['name'])
    return None
"""
# endregion
"""