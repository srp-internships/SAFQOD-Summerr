from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register("reservations", viewset=views.ReservationViewSet)

app_name = "reservation"

urlpatterns = [
    path(
        "",
        include(router.urls),
    )
]
