from django.db import models
from django.contrib.auth import get_user_model
from room.models import Room

User = get_user_model()


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    def __str__(self):
        return f"Reservation for {self.user} in {self.room}"

    class Meta:
        verbose_name = "User Reservation"
        verbose_name_plural = "User Reservations"
