from django.db import models
from django.contrib.auth.models import User

class Ride(models.Model):
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('matched', 'Matched'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    rider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rider_rides")
    driver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="driver_rides")
    pickup_location = models.CharField(max_length=255)
    dropoff_location = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ride {self.id} - {self.status}"

class RiderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="rider_profile")
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username

class DriverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="driver_profile")
    vehicle_name = models.CharField(max_length=100)
    current_location = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} - {self.vehicle_name}"