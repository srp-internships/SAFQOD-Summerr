from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from room import models
from room.serializers import RoomSerializer

ROOM_URLS = reverse("room:room-list")


def detail_url(room_id):
    return reversed("room:room-detail", args=[room_id])


def create_room(user, **params):
    """Create and return a sample room instance"""
    defaults = {
        "name": "Sample room name",
        "descriptions": "Sample room description",
        "volume": 2,
    }
    defaults.update(params)

    room = models.Room.objects.create(user=user, **defaults)

    return room


class PublicRoomAPITest(TestCase):
    """Unauthenticated API requests for room"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication is required for retrieving rooms"""
        res = self.client.get(ROOM_URLS)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRoomAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="testpass123",
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_rooms(self):
        """Test retrieving rooms"""
        create_room(user=self.user)
        create_room(user=self.user)

        res = self.client.get(ROOM_URLS)

        rooms = models.Room.objects.all().order_by("id")
        serializer = RoomSerializer(rooms, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_room_list_limited_to_user(self):
        """Test that rooms are listed only for the authenticated user"""
        user2 = get_user_model().objects.create_user(
            email="user2@example.com",
            password="testpass456",
        )

        create_room(user=self.user)
        create_room(user=user2)

        res = self.client.get(ROOM_URLS)

        rooms = models.Room.objects.filter(user=self.user).order_by("id")
        serializer = RoomSerializer(rooms, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), len(serializer.data))
        self.assertEqual(res.data, serializer.data)

    def test_get_room_detail(self):
        """test to get room detail"""

        room = create_room(user=self.user)

        url = detail_url(room_id=room.id)

        self.client.get(url)
        serializer = RoomDetailSerializer(room)

        self.assertEqual(res.data, serializer.data)
