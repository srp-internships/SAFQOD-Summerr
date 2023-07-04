from django.db import models
from common.models import BaseModel, IsActive
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()


class Room(BaseModel, IsActive):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    volume = models.PositiveIntegerField(blank=True, null=True, verbose_name="Объем")

    def __str_(self):
        return self.name

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
