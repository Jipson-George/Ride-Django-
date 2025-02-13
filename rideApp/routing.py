


from django.urls import re_path

from rideApp.views import LocationConsumer


websocket_urlpatterns = [
    re_path('ws/rides/<int:ride_id>/track/', LocationConsumer.as_asgi())
]