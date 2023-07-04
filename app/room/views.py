from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from room.models import Room
from .serializers import (
    RoomSerializer,
    RoomDetailSerializer,
)


class RoomAPIViewSet(viewsets.ModelViewSet):
    """View for room API list"""

    serializer_class = RoomDetailSerializer
    queryset = Room.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Room.objects.filter(user=user).order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return RoomSerializer
        return self.serializer_class
