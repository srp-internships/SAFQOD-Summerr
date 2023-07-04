from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
router = DefaultRouter()
router.register('rooms', viewset=views.RoomAPIViewSet)

app_name = "room"

urlpatterns = [
    path('', include(router.urls))
]
