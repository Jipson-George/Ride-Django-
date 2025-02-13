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




