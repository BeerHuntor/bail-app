from django.urls import path
from authentication.views import index_view, discord_login, discord_login_callback, discord_register, discord_register_callback, authenticate_user

app_name = 'authentication'
urlpatterns = [
    path('', index_view, name="index"),
    path('login/', discord_login, name='discord_login'),
    path('oauth2/login', discord_login_callback, name='discord_login_callback'),
    path('register/', discord_register, name='discord_register'),
    path('oauth2/register', discord_register_callback, name='discord_register_callback'),

]

