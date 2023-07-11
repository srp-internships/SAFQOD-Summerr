from rest_framework import serializers
from reservation.models import Reservation
from room.models import Room
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class ReservationSerializer(serializers.ModelSerializer):
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Reservation
        fields = ("room", "is_room_occupied", "start_datetime", "end_datetime")

    def get_is_room_occupied(self, obj):
        now = serializers.DateTimeField().to_representation(timezone.now())
        reservations = obj.room.reservations.filter(
            start_datetime__lte=now, end_datetime__gte=now
        )
        return reservations.exists()

    def validate_room(self, room):
        if self.get_is_room_occupied(room):
            raise serializers.ValidationError("The room is already occupied.")
        return room
