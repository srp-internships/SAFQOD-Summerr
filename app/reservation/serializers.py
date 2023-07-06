from rest_framework import serializers


from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    """serializer for reservation"""

    class Meta:
        model = Reservation
        fields = ["id", "user", "room", "start_datetime", "end_datetime"]
        read_only_fields = ("id",)


