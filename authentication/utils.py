import requests
import os
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from datetime import datetime, timedelta

from django.conf import settings
from urllib.parse import urljoin

from authentication.roles_config import ROLE_ID_TO_NAME

class CustomErrorResponse:
    def __init__(self, success, data=None, error_message=None):
        self.success = success
        self.data = data
        self.error_message = error_message

# Discord API Function
def get_request_discord_api_json(endpoint, headers):
    discord_api_url = 'https://discordapp.com/api/'

    """
    with how urljoin works. It doesn't just concatenate strings; it considers the provided endpoint as an absolute URL if it starts with a slash (/),
    overriding the base URL. To ensure correct URL construction, you should handle the concatenation manually when the endpoint starts with a slash.
    """
    if endpoint.startswith('/'):
        full_url = discord_api_url + endpoint
    else: 
        full_url = urljoin(discord_api_url, endpoint)

    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        try:
            # We have a response
            return response.json()
        except ValueError as e:
            error_message = f'JSON decode error: {str(e)}. Raw response: {response.text}'
            return CustomErrorResponse(success=False, error_message=error_message)
    else: 
        error_message = f'Error: {response.status_code}, {response.text}'
        return CustomErrorResponse(success=False, error_message=error_message)

# Time and Date utility
def calculate_token_expiry(expires_in):
    current_time = datetime.now()

    duration = timedelta(seconds=expires_in)

    return current_time + duration

# Returns discord profile picture from url using disord_id and avatar, and downloads it if one doesn't already exist.
def get_discord_profile_pic(discord_id, avatar):

    file_name = f'{discord_id}_{avatar}.png'
    directory = f'media/profile_pics'
    file_path = os.path.join(directory, file_name)
    
    #Check if file already exists. 
    if os.path.exists(file_path):
        print('Profile Picture Exists!')
        return open(file_path, 'rb')
    else:
        print('Downloading the profile picture')
        # Download the file
        profile_pic_url = f'https://cdn.discordapp.com/avatars/{discord_id}/{avatar}.png'
        response = requests.get(profile_pic_url)
        
        if response.status_code == 200:            
            img = Image.open(BytesIO(response.content))
            img.save(file_path, format='PNG')
            #img_content = ContentFile(img_io.getvalue(), f'{discord_id}_{avatar}.png')
            print('saving the profile picture')
            return open(file_path, 'rb')
        
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
    token_endpoint = 'https://discordapp.com/api/oauth2/token'
    

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
    user_data_endpoint = 'users/@me'

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
    guild_id = 1230652347278032936
    # Guild Information
    guild_member_endpoint = f'/users/@me/guilds/{guild_id}/member'
    
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
 
def get_guild_roles(guild_id):
    guild_roles_endpoint = f'/guilds/{guild_id}/roles'
    bot_token = os.getenv('DISCORDBOT_TOKEN')

    headers = {
        'Authorization' : f'Bot {bot_token}'
    }

    roles_data = get_request_discord_api_json(guild_roles_endpoint, headers=headers)
    return roles_data if not isinstance(roles_data, CustomErrorResponse) else roles_data



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
    role_id = get_dictionary_key_from_value(ROLE_ID_TO_NAME, 'NEERP Police') # NEERP Police Role

    guild_user_data = get_user_guild(user_data['access_token'])
    
    if isinstance(guild_user_data, CustomErrorResponse):
        print(f'Error retrieving guild data: {guild_user_data.error_message}, {guild_user_data.error_message.text}')
        return False
    
    user_guild_roles = get_user_guild_roles(guild_user_data)

    if isinstance(user_guild_roles, CustomErrorResponse):
        print(f'Error retrieving user guild roles: {user_guild_roles.error_message}, {user_guild_roles.error_message.text}')
        return False
    
    for role in user_guild_roles:
        if role == role_id:
            return True
        
    return False


def get_role_name_by_id(role_id, guild_roles):
    for role in guild_roles:
        if role['id'] == str(role_id):
            return role['name']
    return None

# Gets user roles for guild
def get_user_guild_roles(user_data):

    if isinstance(user_data, CustomErrorResponse):
        # Handle the error case
        print(f'Error retrieving roles: {user_data.error_message}')
        return[]
    
    role_ids = user_data.get('roles', [])
    return role_ids

# checks the database for the registered user if it exists, and returns none if doesn't
def get_registereduser_if_exist(user):
    from authentication.models import RegisteredUser # Dynamic import to avoid circular import issues
    try:
        return RegisteredUser.objects.get(user=user)
    except RegisteredUser.DoesNotExist:
        return None

def get_dictionary_key_from_value(dict, value):
    for key, val in dict.items():
        if val == value:
            return key
    return None
"""
# endregion
"""