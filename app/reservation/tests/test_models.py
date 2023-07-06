from django.test import TestCase
from django.contrib.auth import get_user_model
from reservation import models
from room.models import Room
import datetime

User = get_user_model()


def create_user(email="user@example.com", password="password123"):
    """Create and return new user or employee"""
    return get_user_model().objects.create(email=email, password=password)


def create_room(user, name="room_name",volume=4 descriptions="Sample description"):
    room = Room.objects.create(
        user=user,
        name=name,
        descriptions=descriptions,
        volume=volume,
    )
    return room


class ReservationModelTest(TestCase):
    """Test model class"""

    def test_create_reservation(self):
        user = create_user()
        room = create_room(user=user)
        start_datetime = datetime.datetime.now()
        end_datetime = start_datetime + datetime.timedelta(hours=1)
        reservation = models.Reservation.objects.create(
            user=user,
            room=room,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        self.assertEqual(reservation.user, user)
        self.assertEqual(reservation.room, room)
        self.assertEqual(reservation.start_datetime, start_datetime)
        self.assertEqual(reservation.end_datetime, end_datetime)
