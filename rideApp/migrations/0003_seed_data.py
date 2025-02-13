from django.db import migrations

def seed_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    RiderProfile = apps.get_model('rideApp', 'RiderProfile')
    DriverProfile = apps.get_model('rideApp', 'DriverProfile')

    # Create users
    user_data = [
        {"id": 2, "username": "rider1", "password": "password123", "is_staff": False},
        {"id": 3, "username": "driver1", "password": "password123", "is_staff": True},
        {"id": 4, "username": "driver2", "password": "password123", "is_staff": True},
        {"id": 5, "username": "driver3", "password": "password123", "is_staff": True},
        {"id": 6, "username": "driver4", "password": "password123", "is_staff": True},
    ]

    created_users = {}
    for user_info in user_data:
        user_obj = User.objects.create_user(
            id=user_info["id"],
            username=user_info["username"],
            password=user_info["password"],
            is_staff=user_info["is_staff"]
        )
        created_users[user_info["id"]] = user_obj

    # Create rider profile
    RiderProfile.objects.create(
        user=created_users[2],
        mobile_number="9876543210",
        address="Bangalore"
    )

    # Create driver profiles
    drivers_data = [
        {"user_id": 3, "vehicle_name": "Toyota Etios", "current_location": "MG Road, Bangalore"},
        {"user_id": 4, "vehicle_name": "Honda City", "current_location": "Koramangala, Bangalore"},
        {"user_id": 5, "vehicle_name": "Maruti Swift", "current_location": "Indiranagar, Bangalore"},
        {"user_id": 6, "vehicle_name": "Hyundai Verna", "current_location": "Whitefield, Bangalore"},
    ]

    for driver_info in drivers_data:
        DriverProfile.objects.create(
            user=created_users[driver_info["user_id"]],
            vehicle_name=driver_info["vehicle_name"],
            current_location=driver_info["current_location"]
        )

def reverse_data(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(id__in=[2, 3, 4, 5, 6]).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('rideApp', '0002_driverprofile_riderprofile'),
    ]

    operations = [
        migrations.RunPython(seed_data, reverse_data),
    ]
