from django.contrib import admin
from django.urls import path, include
from .views import welcome_view, home_view

urlpatterns = [
    path('', welcome_view, name='welcome'),
    path('home/', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('admin/', admin.site.urls),
]