
from django.contrib.auth import get_user_model
from django.db import transaction

from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    VerifyEmailSerializer,
)
from .services import reset_password, verify_email_verification_token
from .tasks import send_email_verification_email, send_password_reset_email


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        # Queue the email only after the database transaction commits.
        transaction.on_commit(
            lambda user_id=user.pk: send_email_verification_email.delay(user_id)
        )


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class MeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "phone": user.phone,
            "role": user.role,
            "is_email_verified": user.is_email_verified,
        })


class RefreshView(TokenRefreshView):
    pass


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            "message": "Successfully logged out."
        })


class VerifyEmailView(generics.GenericAPIView):
    serializer_class = VerifyEmailSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        verify_email_verification_token(serializer.validated_data["token"])

        return Response({"message": "Email verified successfully."})


class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        User = get_user_model()
        user = User.objects.filter(
            email=serializer.validated_data["email"],
            is_active=True,
        ).first()

        # Always respond the same way regardless of whether the account
        # exists, so this endpoint can't be used to enumerate emails.
        if user is not None:
            transaction.on_commit(
                lambda user_id=user.pk: send_password_reset_email.delay(user_id)
            )

        return Response({
            "message": "If an account exists for that email, a reset link has been sent."
        })


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        reset_password(
            serializer.validated_data["token"],
            serializer.validated_data["password"],
        )

        return Response({"message": "Password reset successfully."})
