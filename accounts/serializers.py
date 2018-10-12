from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Profile
from django.contrib.gis.geos import Point


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('location',)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        max_length=32,
        validators=[UniqueValidator(queryset=User.objects.all())]

    )
    password = serializers.CharField(min_length=8, write_only=True)
    profile = ProfileSerializer(required=True)

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])
        profile_data = validated_data.pop('profile')
        location = Point(x=float(profile_data['location']['lat']),
                         y=float(profile_data['location']['lon']), srid=4326)
        Profile.objects.create(user=user, location=location)
        return user

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'profile',)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def _validate_username(self, username, password):
        user = None

        if username and password:
            user = authenticate(username=username, password=password)

        return user

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = self._validate_username(username, password)
        attrs['user'] = user
        return attrs
