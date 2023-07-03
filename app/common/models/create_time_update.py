from django.db import models


class CreateTimeUpdate(models.Model):
    """
        Abstract class with create time and update time
    """
    create_time = models.DateTimeField(verbose_name="Date created", auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="Date updated", auto_now=True)

    class Meta:
        ordering = ['-create_time']
        abstract = True
