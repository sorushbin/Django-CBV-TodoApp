from django.urls import path
from .views import CustomLoginView, CustomRegisterView
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', CustomRegisterView.as_view(), name='register'),
]