from django.urls import path
from .views import home
from django.contrib.auth.forms import UsernameField

urlpatterns = [
    path('', home, name='home-page'),
]
