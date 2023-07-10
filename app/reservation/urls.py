from django.urls import path, include
from reservation.views import ReservationViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
