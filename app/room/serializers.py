from rest_framework import serializers
from .models import Room
from django.utils import timezone


class RoomSerializer(serializers.ModelSerializer):
    is_room_occupied = serializers.SerializerMethodField()

    class Meta:
        model = Room
        fields = ["id", "name", "volume", "is_room_occupied"]
        read_only_fields = ["id", "is_room_occupied"]

    def get_is_room_occupied(self, obj):
        now = serializers.DateTimeField().to_representation(timezone.now())
        reservations = obj.reservations.filter(
            start_datetime__lte=now, end_datetime__gte=now
        )
        return reservations.exists()


class RoomDetailSerializer(RoomSerializer):
    class Meta(RoomSerializer.Meta):
        fields = RoomSerializer.Meta.fields + ["descriptions"]
