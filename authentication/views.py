from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.urls import reverse_lazy
from authentication.forms import SignupForm, CustomAuthenticationForm


class SignupPageView(CreateView):
    form_class = SignupForm
    success_url = reverse_lazy('login')
    template_name = 'authentication/signup.html'


class CustomLoginView(LoginView):
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm



