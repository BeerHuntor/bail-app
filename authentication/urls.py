from django.urls import path
from authentication.views import index_view

urlpatterns = [
    path('', index_view, name="index"),
]
