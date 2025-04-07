from django.contrib import admin
from django.urls import path, include
from .views import welcome_view, home_view, garden_view

#* API *#
from .views import api_test, sensor_working, sensor_warning, check_sensor, new_sensor, add_garden, show_all



urlpatterns = [
    #** Views **#
    path('', welcome_view, name='welcome'),
    path('home/', home_view, name='home'),
    path('accounts/', include('accounts.urls')),
    path('garden/', garden_view, name='garden'),
    
    #** API **#
    path("api/api_test/", api_test, name="api_test"),
    path("api/show_all/", show_all, name="show_all"),
    path("api/sensor_working/<int:raspberry_id>/<int:sensor_id>/", sensor_working, name="sensor_working"),
    path("api/sensor_warning/<int:raspberry_id>/<int:sensor_id>/<str:warning_message>/", sensor_warning, name="sensor_warning"),
    path("api/check_sensor/", check_sensor, name="check_sensor"),
    path("api/new_sensor/<int:raspberry_id>/", new_sensor, name="new_sensor"),
    path("api/add_garden/<int:raspberry_id>/", add_garden, name="add_garden"),

    #** Admin **#
    path('admin/', admin.site.urls),
]