from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth import login
from authentication.forms import SignupForm, CustomAuthenticationForm


class SignupPageView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('home')
    template_name = 'authentication/signup.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm



