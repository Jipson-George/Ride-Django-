from django.conf import settings
from django.urls import path, re_path
from rest_framework.routers import DefaultRouter
from rideApp.views import (
    RegisterView, LoginView,
    RideViewSet,RideStatusUpdateViewSet, DriverMatchingViewSet
    
)
from rest_framework_simplejwt.views import TokenRefreshView
from rideApp.views import LocationConsumer
router = DefaultRouter()
router.register(r'rides', RideViewSet, basename='rides')
router.register(r'drivers', DriverMatchingViewSet)

urlpatterns = [
    # Authentication URLs
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('rides/', RideViewSet.as_view({'get': 'list', 'post': 'create'}), name='ride-list'),
     path('rides/<int:pk>/update-status/', RideStatusUpdateViewSet.as_view({'patch': 'update_status'}), name='ride-status-update'),
    path('drivers/match_driver/', DriverMatchingViewSet.as_view({'post':'match_driver'}), name='driver_match'),
    path('driver/<int:pk>/accept_ride/', DriverMatchingViewSet.as_view({'post':'accept_ride'}), name='accept_ride')]
    #  path('ws/rides/<int:ride_id>/track/', LocationConsumer.as_asgi())]
    # path('rides/<int:pk>/track/', RideTrackingViewSet.as_view({'post': 'update_location'}), name='ride-tracking'),]

websocket_urlpatterns = [
    re_path(r"ws/rides/(?P<ride_id>\d+)/track/$", LocationConsumer.as_asgi()),
]

# Conditionally include WebSocket URLs if running in ASGI mode
if settings.USE_ASGI:
    urlpatterns += websocket_urlpatterns