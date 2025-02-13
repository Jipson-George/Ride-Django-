from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.db import transaction
from rideApp.models import Ride

@override_settings(DATABASES={'default': {'ATOMIC_REQUESTS': True}})
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
        with transaction.atomic():  # Ensures transactions are handled properly
            data = {
                'pickup_location': 'New Pickup',
                'dropoff_location': 'New Dropoff',
                'status': 'REQUESTED'
            }
            response = self.client.post(self.ride_url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertTrue(Ride.objects.filter(pickup_location="New Pickup").exists())

    def test_list_rides(self):
        response = self.client.get(self.ride_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_ride(self):
        response = self.client.get(self.ride_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@override_settings(DATABASES={'default': {'ATOMIC_REQUESTS': True}})
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
        with transaction.atomic():
            data = {'status': 'COMPLETED'}
            response = self.client.patch(self.status_update_url, data)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(Ride.objects.filter(status='COMPLETED').exists())

    def test_update_ride_status_invalid_status(self):
        with transaction.atomic():
            data = {'status': 'INVALID_STATUS'}
            response = self.client.patch(self.status_update_url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_ride_status_unauthenticated(self):
        with transaction.atomic():
            self.client.force_authenticate(user=None)
            data = {'status': 'COMPLETED'}
            response = self.client.patch(self.status_update_url, data)
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
