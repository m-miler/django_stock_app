from django.urls import path
from django.contrib.auth.forms import UsernameField
from dashboard.views import Dashboard, home

urlpatterns = [
    path('', home, name='home'),
    path('dashboard/<str:ticker>', Dashboard.as_view(), name='dashboard'),
]
