from django.contrib import admin
from django.urls import path, include
from .views import welcome_view, home_view, garden_view, activate_sensor, deactivate_sensor

#* API *#
from .views import setup, sensor_working, sensor_warning, check_sensor, new_sensor, add_garden, show_all, delete_all



urlpatterns = [
    #** Views **#
    path('', welcome_view, name='welcome'),
    path('home/', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('garden/<int:garden_id>/', garden_view, name='garden'),
    path('activate_sensor/<int:sensor_id>/<int:garden_id>/', activate_sensor, name='activate_sensor'),
    path('deactivate_sensor/<int:sensor_id>/<int:garden_id>/', deactivate_sensor, name='deactivate_sensor'),
    
    #** TEST API **#
    path("api/setup/", setup, name="setup"),
    path("api/show_all/", show_all, name="show_all"),
    path("api/delete_all/", delete_all, name="delete_all"),

    #** API **#
    path("api/sensor_working/<int:raspberry_id>/<int:sensor_id>/", sensor_working, name="sensor_working"),
    path("api/sensor_warning/<int:raspberry_id>/<int:sensor_id>/<str:warning_message>/", sensor_warning, name="sensor_warning"),
    path("api/check_sensor/", check_sensor, name="check_sensor"),
    path("api/new_sensor/", new_sensor, name="new_sensor"),
    path("api/add_garden/", add_garden, name="add_garden"),

    #** Admin **#
    path('admin/', admin.site.urls),
]