from .uuid import UUIDModel
from .names_descriptions import NamesDescriptions
from .create_time_update import CreateTimeUpdate


class BaseModel(UUIDModel, NamesDescriptions, CreateTimeUpdate):
    """
    Abstract Base model with uuid pk and create and update time
    """

    class Meta:
        abstract = True
