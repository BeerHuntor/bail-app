from django.urls import path
from authentication.views import index_view, login_modal, discord_link, discord_link_callback, discord_login, discord_login_callback, discord_register, discord_register_callback, RegisterModalView

app_name = 'authentication'
urlpatterns = [
    path('', index_view, name="index"),
    path('login/', login_modal, name='login'),
    path('register/', RegisterModalView.as_view(), name='register'),
    path('accounts/discord/link/', discord_link, name="discord_link"), # We bypass this via the below callback
    path('accounts/discord/link/callback/', discord_link_callback, name="discord_link_callback"),
    path('accounts/dscord/login', discord_login, name='discord_login'),
    path('accounts/discord/login/callback', discord_login_callback, name='discord_login_callback'),
    path('accounts/discord/register', discord_register, name='discord_register'),
    path('accounts/discord/register/callback', discord_register_callback, name='discord_register_callback'),
]
