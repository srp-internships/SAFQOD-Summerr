from django.test import TestCase
from django.contrib.auth import get_user_model
from room import models

User = get_user_model()


class RoomModelTest(TestCase):
    """Test Room model"""

    def test_create_room(self):
        """Test creating a room is successful."""
        user = User.objects.create_user(
            email='test@example.com',
            password='testpass123',
        )
        room = models.Room.objects.create(
            user=user,
            name='Sample room name',
            descriptions='Sample room description.',
        )
        self.assertEqual(str(room), room.name)
