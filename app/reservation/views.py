from rest_framework import mixins, viewsets
from reservation.models import Reservation
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import ReservationSerializer


class ReservationViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filter queryset for authenticated users"""
        user = self.request.user
        return Reservation.objects.filter(user=user).order_by("-name")
