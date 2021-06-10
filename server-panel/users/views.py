from users.models import User
from users.serializers import UserSerializer, UserListSerializer, SignInSerializer
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt import tokens

# Create your views here.


class UserList(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserListSerializer


class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdate(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserSignIn(APIView):
    def post(self, request, format=None):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(email=request.data['email'])
            content = {
                'access_token': str(tokens.AccessToken.for_user(user)),
                'refresh_token': str(tokens.RefreshToken.for_user(user)),
                'user': UserSerializer(user).data
            }

            return Response(content, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)