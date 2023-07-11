from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from room.models import Room
from .serializers import RoomSerializer, RoomDetailSerializer

from django.db.models import Q
from django.utils import timezone


class IsSuperUserOrReadOnly(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method in ["PUT", "PATCH", "POST", "DELETE"]:
            return request.user.is_superuser
        return True


class RoomAPIViewSet(viewsets.ModelViewSet):
    """View for room API list"""

    serializer_class = RoomDetailSerializer
    queryset = Room.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsSuperUserOrReadOnly]
    http_method_names = ["get", "put", "patch", "post", "delete"]

    def get_queryset(self):
        return Room.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return RoomSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
