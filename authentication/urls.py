from django.urls import path
from authentication.views import index_view, login_modal

app_name = 'authentication'
urlpatterns = [
    path('', index_view, name="index"),
    path('login/', login_modal, name='login'),
]
