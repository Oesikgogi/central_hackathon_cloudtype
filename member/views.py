# community/member/views.py

from django.shortcuts import render
from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .serializers import SignupSerializer, UserSerializer
from .models import CustomUser
from board.models import Post
from board.serializers import PostSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError
from datetime import datetime

class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.save()
        headers = self.get_success_headers(request.data)
        response_data = {
            'access': user_data['access'],
            'refresh': user_data['refresh'],
            'user': user_data['user']
        }
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

class LoginView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return Response({"detail": "Authorization header is required."}, status=status.HTTP_400_BAD_REQUEST)

            access_token = auth_header.split(' ')[1]
            token = AccessToken(access_token)

            # OutstandingToken 인스턴스 생성 또는 검색
            outstanding_token, created = OutstandingToken.objects.get_or_create(
                token=str(token),
                defaults={
                    'expires_at': datetime.fromtimestamp(token['exp']),
                    'jti': token['jti'],
                    'user': request.user,
                }
            )

            # BlacklistedToken 인스턴스 생성
            BlacklistedToken.objects.get_or_create(
                token=outstanding_token
            )

            return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserInfoView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        profile = instance.profile
        response_data = {
            'id': instance.id,
            'username': instance.username,
            'nickname': profile.nickname,
        }
        return Response(response_data)

class UserPostsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        response_data = [
            {
                "id": post.id,
                "user": post.user.id,
                "title": post.title,
                "created_at": post.created_at.strftime("%Y-%m-%d")
            }
            for post in queryset
        ]
        return Response(response_data, status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
