from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


class Photo(models.Model):
    """
    Represents a photo uploaded by a user, which can be associated with a ticket or review.

    Attributes:
        image (ImageField): The image file uploaded by the user, optional.
        uploader (ForeignKey): The user who uploaded the photo.
        date_created (DateTimeField): Timestamp of when the photo was uploaded.
    """

    image = models.ImageField(blank=True)
    uploader = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)


class Ticket(models.Model):
    """
    Represents a support ticket created by a user.

    Attributes:
        title (CharField): The title of the ticket.
        author (CharField): The name of the author of the ticket. This field is optional.
        description (TextField): A description providing more details about the ticket.
        user (ForeignKey): A reference to the user who created the ticket.
        image (ForeignKey): A reference to an optional photo linked to the ticket.
        time_created (DateTimeField): The timestamp when the ticket was created.
    """

    title = models.CharField(max_length=128)
    author = models.CharField(max_length=128, null=True)
    description = models.TextField(max_length=2048, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ForeignKey(Photo, null=True, on_delete=models.SET_NULL, blank=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
    """
    Represents a review left by a user on a ticket.

    Attributes:
        ticket (ForeignKey): A reference to the ticket being reviewed.
        rating (PositiveSmallIntegerField): A rating for the ticket, between 0 and 5.
        headline (CharField): The title or headline of the review.
        body (TextField): The body or content of the review. This field is optional.
        user (ForeignKey): A reference to the user who wrote the review.
        time_created (DateTimeField): The timestamp when the review was created.
    """

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    headline = models.CharField(max_length=128)
    body = models.TextField(max_length=8192, blank=True)
    user = models.ForeignKey(to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField(auto_now_add=True)
