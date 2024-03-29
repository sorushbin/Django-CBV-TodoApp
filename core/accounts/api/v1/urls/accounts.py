from django.urls import path, include
from .. import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # register
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # change password
    path('change-password', views.ChangePasswordApiView.as_view(), name='change-password'),
    
    # Token Based Authentication
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),

    # JSON Web Token Authentication
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

]