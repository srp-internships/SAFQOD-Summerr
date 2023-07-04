from rest_framework import serializers
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"
        readonly_felds = [
            "id",
        ]

# class RoomDetailSerializer(RoomSerializer):
#     class Meta(RoomSerializer.Meta):
#         fields =