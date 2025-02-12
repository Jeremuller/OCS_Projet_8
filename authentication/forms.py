from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from authentication.models import User
from django import forms


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update(
            {
                "placeholder": "Nom d'utilisateur",
                "autocomplete": "off",
                "class": "form-control w-90",
            }
        )
        self.fields["password"].widget.attrs.update(
            {
                "placeholder": "Mot de passe",
                "autocomplete": "off",
                "class": "form-control w-90",
            }
        )


class FollowUsersForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label="Nom d'utilisateur",
        widget=forms.TextInput(attrs={"placeholder": "Nom d'utilisateur à suivre"}),
    )

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop("request_user", None)
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            user_to_follow = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Cet utilisateur n'existe pas.")

        if user_to_follow == self.request_user:
            raise forms.ValidationError("Vous ne pouvez pas vous suivre vous-même.")

        if self.request_user.follows.filter(id=user_to_follow.id).exists():
            raise forms.ValidationError(f"Vous vuivez déjà {username}")

        return user_to_follow
