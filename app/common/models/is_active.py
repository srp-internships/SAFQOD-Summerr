from django.db import models


class IsActive(models.Model):
    is_active = models.BooleanField(default=False, verbose_name='Is_active: ')

    class Meta:
        abstract = True
