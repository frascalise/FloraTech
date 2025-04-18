from django.contrib import admin
from django.urls import path, include
from .views import get_daily_water_needs, welcome_view, home_view, garden_view, settings_view, edit_sensor, activate_sensor, deactivate_sensor, edit_garden, delete_garden, new_garden

#* API *#
from .views import setup, sensor_working, sensor_warning, check_sensor, new_sensor, add_garden, show_all, delete_all, add_moisture, get_temperature, get_water



urlpatterns = [
    #** Views **#
    path('', welcome_view, name='welcome'),
    path('home/', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('garden/<int:garden_id>/', garden_view, name='garden'),
    path('garden/<int:garden_id>/settings/', settings_view, name='settings'),
    path('edit/<int:garden_id>/', edit_garden, name='edit_garden'),
    path('edit_sensor/<int:sensor_id>/<int:garden_id>/', edit_sensor, name='edit_sensor'),
    path('add_garden/', new_garden, name='add_garden'),
    path('delete/<int:garden_id>/', delete_garden, name='delete_garden'),
    path('activate_sensor/<int:sensor_id>/<int:garden_id>/', activate_sensor, name='activate_sensor'),
    path('deactivate_sensor/<int:sensor_id>/<int:garden_id>/', deactivate_sensor, name='deactivate_sensor'),
    
    #** TEST API **#
    path("api/setup/", setup, name="setup"),
    path("api/show_all/", show_all, name="show_all"),
    path("api/delete_all/", delete_all, name="delete_all"),

    #** API **#
    path("api/sensor_working/<int:raspberry_id>/<int:sensor_id>/", sensor_working, name="sensor_working"),
    path("api/sensor_warning/<int:raspberry_id>/<int:sensor_id>/<str:warning_message>/", sensor_warning, name="sensor_warning"),
    path("api/check_sensor/<int:raspberry_id>", check_sensor, name="check_sensor"),
    path("api/new_sensor/<int:raspberry_id>", new_sensor, name="new_sensor"),
    path("api/add_garden/<int:raspberry_id>", add_garden, name="add_garden"),
    path("api/add_moisture/<int:raspberry_id>", add_moisture, name="add_moisture"),
    path("api/get_daily_water/<int:raspberry_id>/<int:garden_id>", get_daily_water_needs, name="get_daily_water"),
    path("api/get_temperature/", get_temperature, name="get_temperature"),
    path("api/get_water/", get_water, name="get_water"),

    #** Admin **#
    path('admin/', admin.site.urls),
    path('weather/',include('weather.urls')),
    path('comunication/',include('Comunication.urls'))
]