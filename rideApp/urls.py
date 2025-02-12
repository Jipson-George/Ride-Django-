from django.urls import path
from rest_framework.routers import DefaultRouter
from rideApp.views import (
    RegisterView, LoginView,
    RideViewSet,RideStatusUpdateViewSet,RideMatchViewSet,RideTrackingViewSet
    
)
from rest_framework_simplejwt.views import TokenRefreshView
router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='rides')
urlpatterns = [
    # Authentication URLs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('rides/', RideViewSet.as_view({'get': 'list', 'post': 'create'}), name='ride-list'),
     path('rides/<int:pk>/update-status/', RideStatusUpdateViewSet.as_view({'patch': 'update_status'}), name='ride-status-update'),
    path('rides/<int:pk>/match/', RideMatchViewSet.as_view({'post': 'match_ride'}), name='ride-match'),
    path('rides/<int:pk>/track/', RideTrackingViewSet.as_view({'post': 'update_location'}), name='ride-tracking'),]