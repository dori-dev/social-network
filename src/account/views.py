from django.views import generic
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect
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
    success_url = reverse_lazy("account:change_password_done")
    template_name = "account/change-password.html"


class ChangePasswordDone(generic.RedirectView):
    def get(self, request):
        messages.add_message(
            request,
            messages.SUCCESS,
            "پسورد ات ما موفقیت تغییر کرد.",
        )
        return redirect('account:dashboard')
