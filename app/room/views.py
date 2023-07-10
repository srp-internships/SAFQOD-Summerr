from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from room.models import Room
from .serializers import (
    RoomSerializer,
    RoomDetailSerializer,
)

from django.db.models import Q
from datetime import datetime
from django.utils import timezone


class RoomAPIViewSet(viewsets.ModelViewSet):
    """View for room API list"""

    serializer_class = RoomDetailSerializer
    queryset = Room.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "put", "patch", "post", "delete"]

    def get_queryset(self):
        user = self.request.user
        now = timezone.now()
        return Room.objects.filter(
            ~Q(
                reservations__start_datetime__lte=now,
                reservations__end_datetime__gte=now,
            )
        ).order_by("id")

    def get_serializer_class(self):
        if self.action == "list":
            return RoomSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
