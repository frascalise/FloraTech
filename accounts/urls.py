from django.urls import path
from . import views
from . import TestBot

app_name = 'accounts'

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"), 
    path(f"{views.TOKEN_ID}/",views.webhook_view,name="telegram"),
    path('set_webhook/',views.set_webhook,name='aggancio')
]