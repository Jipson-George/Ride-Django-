from rest_framework import serializers
from django.contrib.auth.models import User
from rideApp.models import Ride

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user

# Login Serializer
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

class RideStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['status']

class RideMatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = ['driver', 'status']