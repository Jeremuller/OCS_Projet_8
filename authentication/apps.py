from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """
    Configuration for the Authentication application.
    This class defines the settings for the Authentication app in the Django project.

    Attributes:
        default_auto_field: The default auto field type for the application.
        name: The name of the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "authentication"
