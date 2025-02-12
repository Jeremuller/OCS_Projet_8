from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from authentication.forms import SignupForm, CustomAuthenticationForm


class SignupPageView(CreateView):
    """
    A view for handling user registration. It uses the SignupForm
    to create a new user, logs the user in, and redirects to the homepage
    upon successful submission.
    """

    # Form used for user registration
    form_class = SignupForm
    # Redirect to the homepage on success
    success_url = reverse_lazy("home")
    # Template for the signup page
    template_name = "authentication/signup.html"

    def form_valid(self, form):
        """
        Override the form_valid method to log the user in immediately after
        successful registration.

        Args:
            form: The form object with valid data.

        Returns:
            HttpResponseRedirect: Redirect to the success URL.
        """
        # Save the user to the database
        user = form.save()
        # Log the user in
        login(self.request, user)
        # Return the normal form_valid response
        return super().form_valid(form)


class CustomLoginView(LoginView):
    """
    A custom login view that overrides the default LoginView. It uses
    CustomAuthenticationForm and redirects authenticated users away from
    the login page.
    """

    # Template for the login page
    template_name = "authentication/login.html"
    # Redirect authenticated users to the homepage
    redirect_authenticated_user = True
    # Form used for user login
    form_class = CustomAuthenticationForm
