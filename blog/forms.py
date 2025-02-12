from django import forms
from . import models


class TicketForm(forms.ModelForm):
    """
    Form for creating or editing a ticket.

    Attributes:
        edit_ticket: Hidden field used to indicate whether the ticket is being edited or created.
    """

    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ["title", "author", "description"]


class DeleteTicketForm(forms.Form):
    """
    Form for deleting a ticket.

    Attributes:
        delete_ticket (BooleanField): Hidden field to indicate that the ticket is to be deleted.
    """

    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    """
    Form for creating or editing a review for a ticket.

    Attributes:
        edit_review (BooleanField): Hidden field to indicate whether the review is being edited or created.
        rating (ChoiceField): A field to select the rating, displayed as radio buttons.
    """

    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ["headline", "rating", "body"]
        labels = {
            "headline": "Titre",
            "body": "Commentaire",
        }

    # Rating field using radio buttons for score selection
    rating = forms.ChoiceField(
        choices=[(i, "- " + str(i)) for i in range(6)],
        widget=forms.RadioSelect(attrs={"class": "inline-radio"}),
        label="Note",
    )


class DeleteReviewForm(forms.Form):
    """
    Form for deleting a review.

    Attributes:
        delete_review (BooleanField): Hidden field to indicate that the review is to be deleted.
    """

    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class PhotoForm(forms.ModelForm):
    """
    Form for adding or editing a photo associated with a review or ticket.

    Attributes:
        'image' (ImageField): A field to upload an image for the ticket or review.
    """

    class Meta:
        model = models.Photo
        fields = ["image"]
