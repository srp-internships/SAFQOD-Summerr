from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from room import models

from room.serializers import RoomSerializer, RoomDetailSerializer

ROOM_URLS = reverse("room:room-list")


def detail_url(room_id):
    """Return URL for room detail"""
    return reverse("room:room-detail", args=[room_id])


def create_room(user, **params):
    """Create and return a sample room instance"""
    defaults = {
        "name": "Sample room name",
        "volume": 2,
    }
    defaults.update(params)

    room = models.Room.objects.create(user=user, **defaults)

    return room


def create_user(**params):
    """create and return a new user"""
    return get_user_model().objects.create(**params)


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
        """Test to get room detail"""
        room = create_room(user=self.user)
        url = detail_url(room_id=room.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        serializer = RoomDetailSerializer(room)
        self.assertEqual(res.data, serializer.data)

    def test_create_room(self):
        payload = {
            "name": "sample name",
            "volume": 3,
        }

        res = self.client.post(ROOM_URLS, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        room = models.Room.objects.get(id=res.data["id"])

        for k, v in payload.items():
            self.assertEqual(getattr(room, k), v)

        self.assertEqual(room.user, self.user)

    def test_partial_upadate(self):
        """test partial update of room"""
        cur_volume = 2
        room = models.Room.objects.create(
            user=self.user, name="sample name", volume=cur_volume
        )
        payload = {
            "name": "new room title",
        }
        url = detail_url(room.id)
        res = self.client.patch(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        room.refresh_from_db(fields=["name"])
        self.assertEqual(room.volume, cur_volume)
        self.assertEqual(room.user, self.user)

    def test_full_update(self):
        room = create_room(
            user=self.user,
            name="new room name",
            volume=2,
            descriptions="new descriptions",
        )

        payload = {
            "name": "new room name",
            "volume": 2,
            "descriptions": "new descriptions",
        }

        url = detail_url(room.id)
        res = self.client.put(url, payload)

        for k, v in payload.items():
            self.assertEqual(getattr(room, k), v)

        self.assertEqual(room.user, self.user)

    def update_user_return_error(self):
        new_user = create_user(email="user2@example", password="test123")
        room = create_room(user=self.user)
        payload = {"user": new_user}

        url = detail_url(room_id=room.id)
        self.client.patch(url, payload)

        room.refresh_from_db()
        self.assertEqual(room.user, self.user)

    def test_delete_room(self):
        room = create_room(user=self.user)

        url = detail_url(room_id=room.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Room.objects.filter(id=room.id).exists())

    def test_delete_other_users_room_error(self):
        new_user = create_user(email="user2@example.com", password="test123")

        room = create_room(user=new_user)
        url = detail_url(room_id=room.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(models.Room.objects.filter(id=room.id).exists())
