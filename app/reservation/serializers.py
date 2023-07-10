from rest_framework import serializers
from reservation.models import Reservation
from room.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()


class ReservationSerializer(serializers.ModelSerializer):
    reserved_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())

    class Meta:
        model = Reservation
        fields = ("id", "reserved_by", "room", "is_room_occupied", "start_datetime", "end_datetime")
