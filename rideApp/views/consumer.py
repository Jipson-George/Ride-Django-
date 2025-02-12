import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rideApp.models import Ride_Location, Ride
from django.utils import timezone

class LocationConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coordinates = [
            {"lat": 12.9716, "lng": 77.5946},  
            {"lat": 13.0083, "lng": 77.6197},  
            {"lat": 13.0455, "lng": 77.6448},  
            {"lat": 13.0641, "lng": 77.6674},  
            {"lat": 13.0827, "lng": 77.6899}   
        ]
        self.current_index = 0

    async def connect(self):
        self.ride_id = self.scope['url_route']['kwargs']['ride_id']
        self.room_group_name = f'ride_{self.ride_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        asyncio.create_task(self.send_location_updates())

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def create_location(self):
        ride = Ride.objects.get(id=self.ride_id)
        print(f"[DEBUG] Current ride status: {ride.status}")
        
        if ride.status == 'completed' or self.current_index >= len(self.coordinates):
            ride.status = 'completed'
            ride.save()
            print("[DEBUG] Ride marked as completed in DB.")
            return None

        current_point = self.coordinates[self.current_index]
        self.current_index += 1

        location = Ride_Location.objects.create(
            ride=ride,
            latitude=current_point["lat"],
            longitude=current_point["lng"],
            location_name=f"Point {current_point['lat']:.4f}, {current_point['lng']:.4f}",
            current_time=timezone.now(),
            destination_latitude=self.coordinates[-1]["lat"],
            destination_longitude=self.coordinates[-1]["lng"]
        )

        print(f"[DEBUG] New Location Saved: ({location.latitude}, {location.longitude})")
        return location

    async def send_location_updates(self):
        while True:
            print("\n[DEBUG] Updating location...")
            
            location = await self.create_location()
            if not location:
                await self.update_ride_status()
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'ride_completed',
                        'message': f'Ride {self.ride_id} has been completed successfully!'
                    }
                )
                print("[DEBUG] Ride completed successfully! Stopping updates.")
                break
                
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'location_update',
                    'latitude': str(location.latitude),
                    'longitude': str(location.longitude),
                    'location_name': location.location_name,
                    'timestamp': str(location.current_time)
                }
            )
            
            print("[DEBUG] WebSocket location update sent.")
            await asyncio.sleep(10)

    async def location_update(self, event):
        await self.send(text_data=json.dumps(event))

    async def ride_completed(self, event):
        await self.send(text_data=json.dumps({'message': event['message']}))
