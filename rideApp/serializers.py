from rest_framework import serializers
from django.contrib.auth.models import User
from rideApp.models import AvailableDriver, Ride

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
class AvailableDriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvailableDriver
        fields = '__all__'

class RideRequestSerializer(serializers.Serializer):
    pickup_latitude = serializers.DecimalField(max_digits=9, decimal_places=6)
    pickup_longitude = serializers.DecimalField(max_digits=9, decimal_places=6)