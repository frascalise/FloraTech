from django.urls import path
from .views import register_view, login_view, logout_view
from . import TestBot

app_name = 'accounts'

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"), 
    path(f"{TestBot.TOKEN}/",TestBot.webhook_view,name="telegram"),
    path('set_webhook/',TestBot.set_webhook,name='aggancio')
]