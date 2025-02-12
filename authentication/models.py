from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extends the built-in User model to add a "follow" feature,
    allowing users to follow other users.

    Attributes:
        follows (ManyToManyField):
            A self-referential Many-to-Many relationship allowing users
            to follow each other. The relation is not symmetrical, meaning
            that if User A follows User B, User B does not automatically follow User A.
    """

    follows = models.ManyToManyField(
        "self",
        symmetrical=False,
        # Display name of the relationship in the admin panel
        verbose_name="suit",
        # Reverse relation to get followers of a user
        related_name="followers",
    )


class UserFollows(models.Model):
    """
    Represents a follow relationship between two users. Each instance tracks
    when a user follows another user.

    Attributes:
        user (ForeignKey):
            The user who is following someone.
        followed_user (ForeignKey):
            The user being followed by the `user`.
    """

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following"
    )

    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        # If the followed user is deleted, remove the following relationship
        on_delete=models.CASCADE,
        # Reverse relation to access users following a specific user
        related_name="followed_by",
    )

    class Meta:
        """
        Metaclass used to enforce that a user can follow another user only once.
        """

        unique_together = (
            "user",
            "followed_user",
        )
