from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authentication.models import User
from django import forms


class SignupForm(UserCreationForm):
    """
    Custom signup form extending Django's UserCreationForm.
    Used to handle the user creation process including the username and password fields.
    """

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form extending Django's AuthenticationForm.
    Used to manage user login and includes custom styling for form fields.
    """

    def __init__(self, *args, **kwargs):
        """
        Customizes the form fields by adding placeholders, autocomplete settings,
        and custom CSS classes for better styling.
        """

        super().__init__(*args, **kwargs)

        # Customize username field appearance
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Nom d'utilisateur",
                "autocomplete": "off",
                "class": "form-control w-90",
            }
        )

        # Customize password field appearance
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Mot de passe",
                "autocomplete": "off",
                "class": "form-control w-90",
            }
        )


class FollowUsersForm(forms.Form):
    """
    Form to allow a user to follow another user by entering their username.
    It validates if the user exists, and checks if the user is already being followed.
    """

    # Username field where the user enters the username of the person they wish to follow
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur à suivre"}),
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the form, accepting the request_user parameter to check who is following.
        """
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        """
        Validates the username entered by the user. Ensures the username exists,
        that the user is not trying to follow themselves, and that they are not
        already following the user.
        """
        username = self.cleaned_data["username"]

        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas.")

        # Check if user is trying to follow themselves
        if user_to_follow == self.request_user:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")

        # Check if the user is already following the target user
        if self.request_user.follows.filter(id=user_to_follow.id).exists():
            raise forms.ValidationError(f"Vous vuivez déjà {username}")

        return user_to_follow
