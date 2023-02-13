from dashboard.views import Dashboard, home
from django.contrib.auth.forms import UsernameField
from django.urls import path

urlpatterns = [
    path("", home, name="home"),
    path("dashboard/<str:ticker>", Dashboard.as_view(), name="dashboard"),
]
