from rest_framework import generics, status
from .serializers import (
    RegistrationSerializer,
    CustomAuthTokenSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    ProfileSerializer,
    ActivationResendSerializer,
    ResetPasswordSerializer,
    ResetPasswordConfirmSerializer,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ...models import Profile
from mail_templated import EmailMessage
from ..utils import EmailThread
import jwt
from jwt.exceptions import ExpiredSignatureError, DecodeError
from django.conf import settings


User = get_user_model()


class RegistrationApiView(generics.GenericAPIView):
    """register users and validated the user data"""

    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data["email"]
            data = {"email": email}
            user_obj = get_object_or_404(User, email=email)
            token = self.get_tokens_for_user(user_obj)
            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "admin@admin.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class CustomObtainAuthToken(ObtainAuthToken):
    """customize obtain auth token"""

    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user_id": user.pk, "email": user.email})


class CustomDiscardAuthToken(APIView):
    """this is for discard token and logout"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordApiView(generics.GenericAPIView):
    """this class is for change password"""

    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["Wrong password."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(generics.RetrieveUpdateAPIView):
    """Retrieve  profile data of authenticated user"""

    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user.id)
        return obj


class ActivationConfirmApiView(APIView):
    """Send activation token for user and verified"""

    def get(self, request, *args, **kwargs):
        token = kwargs.get("token")
        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decode_token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DecodeError:
            return Response(
                {"details": "token is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        user_obj = User.objects.get(pk=user_id)
        if user_obj.is_verified:
            return Response({"details": "Your account has already verified."})
        user_obj.is_verified = True
        user_obj.save()
        return Response(
            {"details": "Your account have been verified and activated successfully."}
        )


class ActivationResendApiView(APIView):
    """resend activation token"""

    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {
                "details": "user activation resend successfully. Please check your mail box."
            },
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordApiView(APIView):
    """this is for forget password and reset its"""

    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_obj = serializer.validated_data["user"]
        token = self.get_tokens_for_user(user_obj)
        email_obj = EmailMessage(
            "email/reset_password_email.tpl",
            {"token": token},
            "admin@admin.com",
            to=[user_obj.email],
        )
        EmailThread(email_obj).start()
        return Response(
            {
                "details": "The password reset link has been sent. Please check your mail box."
            },
            status=status.HTTP_200_OK,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class ResetPasswordConfirm(generics.GenericAPIView):
    """Password reset confirm view"""

    serializer_class = ResetPasswordConfirmSerializer

    def put(self, request, *args, **kwargs):
        token = kwargs.get("token")
        try:
            decode_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = decode_token.get("user_id")
        except ExpiredSignatureError:
            return Response(
                {"details": "token has been expired."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except DecodeError:
            return Response(
                {"details": "token is not valid."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # email = User.objects.get(pk=user_id).email
        user_obj = User.objects.get(pk=user_id)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_obj.set_password(serializer.data.get("new_password"))
            user_obj.save()
            return Response(
                {"details": "password changed successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
