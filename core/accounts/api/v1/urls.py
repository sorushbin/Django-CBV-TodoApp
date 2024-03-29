from django.urls import path, include
from . import views

urlpatterns = [
    # register
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),


]