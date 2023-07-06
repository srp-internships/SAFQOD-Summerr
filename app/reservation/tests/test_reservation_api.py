from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from reservation.models import Reservation
from room.models import Room
from reservation.serializers import ReservationSerializer

TAG_URL = reverse("reservation:reservation-list")


def create_user(email="user@example.com", password="password123"):
    return get_user_model().objects.create(email=email, password=password)


def create_room(user, name="room_name", volume=10, descriptions="Sample description"):
    return Room.objects.create(
        user=user, name=name, volume=volume, descriptions=descriptions
    )


class PublicReservedAPITest(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.user = create_user()
        self.room = create_room(self.user)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_reserved_list(self):
        """Test retrieving a list of reservations"""
        Reservation.objects.create(
            user=self.user,
            room=self.room,
            start_datetime="2023-07-01T10:00:00",
            end_datetime="2023-07-01T11:00:00",
        )

        response = self.client.get(TAG_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_reserved_successful(self):
        """Test creating a new reservation"""
        payload = {
            "user": self.user.id,
            "room": self.room.id,
            "start_datetime": "2023-07-01T10:00:00",
            "end_datetime": "2023-07-01T11:00:00",
        }

        response = self.client.post(TAG_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        reservation = Reservation.objects.get(id=response.data["id"])
        serializer = ReservationSerializer(reservation)
        self.assertEqual(response.data, serializer.data)
