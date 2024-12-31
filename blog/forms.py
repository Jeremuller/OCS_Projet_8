from django import forms
from . import models


class TicketForm(forms.ModelForm):
    edit_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Ticket
        fields = ['title', 'author', 'description']


class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    edit_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)

    class Meta:
        model = models.Review
        fields = ['rating', 'headline', 'body']

    rating = forms.ChoiceField(
        choices=[(i, str(i)) for i in range(6)],
        widget=forms.RadioSelect,
        label="Note",
    )


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class PhotoForm(forms.ModelForm):
    class Meta:
        model = models.Photo
        fields = ['image']



    