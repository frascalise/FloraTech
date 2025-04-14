from django.urls import path
from .views import register_view, login_view, logout_view
from . import BOT

urlpatterns = [
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"), 
    path(f"{BOT.TOKEN}/",BOT.webhook_view,name="telegram")  
]