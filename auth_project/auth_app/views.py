# auth_app/views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import User, OTP
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
import random

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user, created = User.objects.get_or_create(email=email)
            if created:
                return Response({"message": "Registration successful. Please verify your email."}, status=status.HTTP_201_CREATED)
            return Response({"message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RequestOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            otp = random.randint(100000, 999999)
            OTP.objects.create(user=user, otp=otp)
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "Email not registered."}, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        otp_input = request.data.get('otp')
        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user).latest('created_at')
            if otp.is_valid() and otp.otp == otp_input:
                refresh = RefreshToken.for_user(user)
                return Response({
                    "message": "Login successful.",
                    "token": str(refresh.access_token)
                }, status=status.HTTP_200_OK)
            return Response({"message": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, OTP.DoesNotExist):
            return Response({"message": "Invalid request."}, status=status.HTTP_400_BAD_REQUEST)
