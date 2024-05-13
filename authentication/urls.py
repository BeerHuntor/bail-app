from django.urls import path
from authentication.views import index_view, login_modal, discord_login, RegisterModalView

app_name = 'authentication'
urlpatterns = [
    path('', index_view, name="index"),
    path('login/', login_modal, name='login'),
    path('register/', RegisterModalView.as_view(), name='register'),
    path('accounts/discord/login/', discord_login, name="discord_login"),
]
