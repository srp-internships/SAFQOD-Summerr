from django.db import models


class NamesDescriptions(models.Model):
    """
    Abstract model with name and description field
    """

    name = models.CharField(max_length=255, verbose_name="Name: ")
    descriptions = models.TextField(
        verbose_name="Descriptions: ", default="no", blank=True
    )

    class Meta:
        abstract = True

    def __str__(self) -> str:
        return self.name
