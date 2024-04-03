from django.urls import path, include
from .. import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


urlpatterns = [
    # register
    path('registration/', views.RegistrationApiView.as_view(), name='registration'),

    # activation
    path('activation/confirm/<str:token>', views.ActivationConfirmApiView.as_view(), name='activation'),
    
    # resend activation token
    path('activation/resend/', views.ActivationResendApiView.as_view(), name='activation-resend'),

    # change password
    path('change-password', views.ChangePasswordApiView.as_view(), name='change-password'),
    
    # reset password
    path('reset-password/', views.ResetPasswordApiView.as_view(), name='reset-password'),
    path('reset-password/confirm/<str:token>', views.ResetPasswordConfirm.as_view(), name='reset-password-confirm'),

    # Token Based Authentication
    path('token/login/', views.CustomObtainAuthToken.as_view(), name='token-login'),
    path('token/logout/', views.CustomDiscardAuthToken.as_view(), name='token-logout'),

    # JSON Web Token Authentication
    path('jwt/create/', views.CustomTokenObtainPairView.as_view(), name='jwt-create'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt-refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt-verify'),

]