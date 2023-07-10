from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from reservation.views import ReservationViewSet
from reservation.models import Reservation
from room.models import Room
from reservation.serializers import ReservationSerializer
from rest_framework import status

User = get_user_model()


class ReservationViewSetTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpass123",
        )
        self.room = Room.objects.create(
            user=self.user,
            name="Sample Room",
            volume=4,
        )
        self.view = ReservationViewSet.as_view({"get": "list", "post": "create"})
        self.url = "/reservations/"

    def test_list_reservations_authenticated(self):
        # Создаем несколько резерваций
        Reservation.objects.create(
            reserved_by=self.user,
            room=self.room,
            start_datetime="2023-07-10T09:00:00Z",
            end_datetime="2023-07-10T12:00:00Z",
        )
        Reservation.objects.create(
            reserved_by=self.user,
            room=self.room,
            start_datetime="2023-07-11T10:00:00Z",
            end_datetime="2023-07-11T13:00:00Z",
        )

        # Аутентифицируем пользователя
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)

        # Выполняем запрос GET к представлению
        response = self.view(request)

        # Проверяем код состояния и данные ответа
        self.assertEqual(response.status_code, 200)
        reservations = Reservation.objects.filter(reserved_by=self.user)
        serializer = ReservationSerializer(reservations, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_list_reservations_unauthenticated(self):
        # Создаем несколько резерваций
        Reservation.objects.create(
            reserved_by=self.user,
            room=self.room,
            start_datetime="2023-07-10T09:00:00Z",
            end_datetime="2023-07-10T12:00:00Z",
        )
        Reservation.objects.create(
            reserved_by=self.user,
            room=self.room,
            start_datetime="2023-07-11T10:00:00Z",
            end_datetime="2023-07-11T13:00:00Z",
        )

        # Выполняем запрос GET к представлению без аутентификации
        request = self.factory.get(self.url)
        response = self.view(request)

        # Проверяем код состояния и данные ответа
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )

    def test_delete_reservation_unauthenticated(self):
        # Создаем резервацию
        reservation = Reservation.objects.create(
            reserved_by=self.user,
            room=self.room,
            start_datetime="2023-07-10T09:00:00Z",
            end_datetime="2023-07-10T12:00:00Z",
        )

        # Выполняем запрос DELETE к представлению без аутентификации
        request = self.factory.delete(f"{self.url}{reservation.id}/")
        response = self.view(request, pk=reservation.id)

        # Проверяем код состояния и данные ответа
        self.assertEqual(response.status_code, 401)
        self.assertEqual(
            response.data, {"detail": "Authentication credentials were not provided."}
        )
