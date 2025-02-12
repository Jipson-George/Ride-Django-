from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import F
from math import radians, sin, cos, sqrt, atan2
from rideApp.models import AvailableDriver
from rideApp.serializers import AvailableDriverSerializer, RideRequestSerializer
from django.utils import timezone
class DriverMatchingViewSet(viewsets.ModelViewSet):
    queryset = AvailableDriver.objects.all()
    serializer_class = AvailableDriverSerializer

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Earth's radius in km
        lat1, lon1, lat2, lon2 = map(radians, [float(lat1), float(lon1), float(lat2), float(lon2)])
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        return R * c

    @action(detail=False, methods=['post'])
    def match_driver(self, request):
        serializer = RideRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        pickup_lat = serializer.validated_data['pickup_latitude']
        pickup_lng = serializer.validated_data['pickup_longitude']

        available_drivers = AvailableDriver.objects.filter(status='available')
        
        if not available_drivers:
            return Response({"message": "No drivers available"}, status=status.HTTP_404_NOT_FOUND)

        # Calculate distances for all available drivers
        drivers_with_distance = []
        for driver in available_drivers:
            distance = self.calculate_distance(
                pickup_lat, 
                pickup_lng, 
                driver.current_latitude, 
                driver.current_longitude
            )
            drivers_with_distance.append({
                'driver': driver,
                'distance': distance
            })

        # Sort by distance first, then by last ride completion time
        sorted_drivers = sorted(
            drivers_with_distance,
            key=lambda x: (x['distance'], x['driver'].last_ride_completed_time or timezone.now())
        )

        matched_driver = sorted_drivers[0]['driver']
        return Response({
            'driver_id': matched_driver.driver.id,
            'distance': sorted_drivers[0]['distance'],
            'current_latitude': matched_driver.current_latitude,
            'current_longitude': matched_driver.current_longitude
        })

    @action(detail=True, methods=['post'])
    def accept_ride(self, request, pk=None):
            try:
                driver = AvailableDriver.objects.get(driver_id=pk)
                if driver.status != 'available':
                    return Response(
                        {"message": "Driver is not available"},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                driver.status = 'busy'
                driver.save()
                return Response({
                    "message": "Ride accepted successfully",
                    "driver_id": driver.driver_id,
                    "current_status": driver.status
                })
            except AvailableDriver.DoesNotExist:
                return Response(
                    {"message": "Driver not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
