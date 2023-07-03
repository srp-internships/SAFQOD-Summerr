from django.db import models
from common.models import BaseModel, IsActive


class Rooms(BaseModel, IsActive):
    volume = models.PositiveIntegerField(blank=True, null=True, verbose_name="Объем")

    class Meta:
        verbose_name = "Комната"
        verbose_name_plural = "Комнаты"
