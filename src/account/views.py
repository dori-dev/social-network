from django.views import generic
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms


class UserLogin(views.LoginView):
    form_class = forms.LoginForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True


class UserLogout(views.LogoutView):
    template_name = 'account/logged_out.html'


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account/dashboard.html'
