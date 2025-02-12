from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    Configuration for the Blog application.
    This class defines the settings for the Blog app in the Django project.

    Attributes:
        default_auto_field: The default auto field type for the application.
        name: The name of the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
