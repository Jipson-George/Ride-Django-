from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rideApp.models import Ride

class RideViewSetTests(TestCase):
    databases = {'default'}
    
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def setUp(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.ride = Ride.objects.create(
            rider=self.user,
            pickup_location='Test Pickup',
            dropoff_location='Test Dropoff',
            status='REQUESTED'
        )
        
        self.ride_url = reverse('rides-list')
        self.ride_detail_url = reverse('rides-detail', args=[self.ride.pk])

    def test_create_ride(self):
        data = {
            'pickup_location': 'New Pickup',
            'dropoff_location': 'New Dropoff',
            'status': 'REQUESTED'
        }
        response = self.client.post(self.ride_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ride.objects.count(), 2)

    def test_list_rides(self):
        response = self.client.get(self.ride_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_ride(self):
        response = self.client.get(self.ride_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class RideStatusUpdateTests(TestCase):
    databases = {'default'}
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.ride = Ride.objects.create(
            rider=self.user,
            pickup_location='Test Pickup',
            dropoff_location='Test Dropoff',
            status='REQUESTED'
        )
        
        self.status_update_url = reverse('ride-status-update', args=[self.ride.pk])

    def test_update_ride_status(self):
        data = {'status': 'COMPLETED'}
        response = self.client.patch(self.status_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_ride_status_invalid_status(self):
        data = {'status': 'INVALID_STATUS'}
        response = self.client.patch(self.status_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ride_status_unauthenticated(self):
        self.client.force_authenticate(user=None)
        data = {'status': 'COMPLETED'}
        response = self.client.patch(self.status_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
