from django.views import generic
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from . import forms


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account/dashboard.html'


class UserLogin(views.LoginView):
    form_class = forms.LoginForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True


class UserLogout(views.LogoutView):
    template_name = 'account/logged_out.html'


class ChangePassword(LoginRequiredMixin, views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    template_name = "account/change-password.html"

    def get_success_url(self) -> str:
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "پسورد ات ما موفقیت تغییر کرد.",
        )
        return reverse('account:dashboard')
