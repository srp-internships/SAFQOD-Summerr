from django.db import models


class IsApproved(models.Model):
    is_approved = models.BooleanField(default=False, verbose_name='Is_approved: ')

    class Meta:
        abstract = True
