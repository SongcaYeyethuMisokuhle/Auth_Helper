from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, ResetPasswordRequestSerializer, ResetPasswordConfirmSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework import status
from django.urls import reverse
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        verify_path = reverse('verify-email')
        verify_url = self.request.build_absolute_uri(f"{verify_path}?uid={uid}&token={token}")
        send_mail(
            'Verify your account',
            f'Click the link to verify your account: {verify_url}',
            None,
            [user.email],
        )

class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        uid = request.query_params.get('uid')
        token = request.query_params.get('token')
        try:
            uid_decoded = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid_decoded)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return Response({'message': 'Email verified successfully!'})
        return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_path = reverse('reset-password-confirm')
                reset_url = request.build_absolute_uri(f"{reset_path}?uid={uid}&token={token}")
                send_mail(
                    'Password Reset',
                    f'Click the link to reset your password: {reset_url}',
                    None,
                    [user.email],
                )
                return Response({'message': 'Password reset link sent if that email exists (for privacy)'})
            except User.DoesNotExist:
                # for privacy, respond the same way whether or not the user exists
                return Response({'message': 'Password reset link sent if that email exists (for privacy)'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                uid = force_str(urlsafe_base64_decode(serializer.validated_data['uid']))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'error': 'Invalid user'}, status=status.HTTP_400_BAD_REQUEST)

            token = serializer.validated_data['token']
            if default_token_generator.check_token(user, token):
                user.set_password(serializer.validated_data['new_password'])
                user.save()
                return Response({'message': 'Password reset successful'})
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# (Optional) simple token-based login is provided by SimpleJWT views via urls.py
