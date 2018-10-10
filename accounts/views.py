from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from accounts.serializers import UserSerializer, LoginSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken


class UserCreate(APIView):

    def post(self, request, format='json'):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                token = Token.objects.create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Login(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data,
                                     context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            if user:
                token, created = Token.objects.get_or_create(user=user)
                json = serializer.data
                json['token'] = token.key
                return Response(json, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):

    def post(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            request.user.auth_token.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
