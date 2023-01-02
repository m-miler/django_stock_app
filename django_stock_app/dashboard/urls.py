from django.urls import path
from django.contrib.auth.forms import UsernameField

urlpatterns = [
    path('dashboard/<str:ticker>', Dashboard.as_view(), name='dashboard'),
]
