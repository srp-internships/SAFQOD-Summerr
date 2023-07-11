from django.db import models
from django.contrib.auth import get_user_model
from room.models import Room
from django.utils import timezone

User = get_user_model()


class Reservation(models.Model):
    reserved_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        related_name="reservations",
    )
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"Резервация для {self.reserved_by} в {self.room}"

    class Meta:
        verbose_name = "Резервация"
        verbose_name_plural = "User Reservations"

    @property
    def is_room_occupied(self):
        now = timezone.now()
        return self.start_datetime <= now <= self.end_datetime
