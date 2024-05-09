from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

app_name = "api-v1"

router = DefaultRouter()
router.register("task", views.TaskModelViewSet, basename="task")


urlpatterns = [
    path("", include(router.urls)),
    path("weather/<str:city_name>", views.WeatherApiView.as_view(), name="weather"),

]
