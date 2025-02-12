from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from rideApp.models import Ride
from rideApp.serializers import RideSerializer, RideStatusSerializer, RideMatchSerializer
import random
import time




class RideViewSet(viewsets.ModelViewSet):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(rider=self.request.user)

class RideStatusUpdateViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def update_status(self, request, pk=None):
        ride = Ride.objects.get(pk=pk)
        serializer = RideStatusSerializer(ride, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Status updated successfully"})
        return Response(serializer.errors, status=400)

class RideMatchViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def match_ride(self, request, pk=None):
        ride = Ride.objects.get(pk=pk)
        if ride.status != "requested":
            return Response({"error": "Ride has already been matched or completed"}, status=400)
        
        available_drivers = User.objects.filter(is_staff=True)  # Assuming drivers are staff users
        if not available_drivers.exists():
            return Response({"error": "No available drivers"}, status=400)

        driver = random.choice(available_drivers)  # Basic ride matching logic
        ride.driver = driver
        ride.status = "matched"
        ride.save()

        return Response({"message": f"Ride matched with Driver {driver.username}"})

class RideTrackingViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def update_location(self, request, pk=None):
        ride = Ride.objects.get(pk=pk)
        if ride.status != "ongoing":
            return Response({"error": "Ride must be ongoing to update location"}, status=400)

        ride.current_location = request.data.get("current_location")
        ride.save()
        return Response({"message": "Ride location updated"})
from rest_framework import viewsets, status
from rest_framework.decorators import action

class DriverManagementViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def toggle_availability(self, request):
        driver = request.user
        if not driver.is_staff:
            return Response({"error": "User is not a driver"}, status=status.HTTP_403_FORBIDDEN)
        
        driver.is_available = not driver.is_available
        driver.save()
        return Response({
            "message": f"Driver availability set to {driver.is_available}"
        })

class RideHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RideSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:  # Driver
            return Ride.objects.filter(driver=user)
        return Ride.objects.filter(rider=user)

    @action(detail=False, methods=['get'])
    def completed_rides(self, request):
        queryset = self.get_queryset().filter(status='completed')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
