from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse
from . import forms


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account/dashboard.html'


class UserLogin(auth_views.LoginView):
    form_class = forms.LoginForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True


class UserLogout(auth_views.LogoutView):
    template_name = 'account/logged_out.html'


class ChangePassword(LoginRequiredMixin, auth_views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    template_name = "account/change-password.html"

    def get_success_url(self) -> str:
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "پسورد ات ما موفقیت تغییر کرد.",
        )
        return reverse('account:dashboard')


class ResetPassword(auth_views.PasswordResetView):
    form_class = forms.ResetPasswordForm
    email_template_name = 'account/reset-password/email.html'
    template_name = 'account/reset-password/form.html'
    subject_template_name = 'account/reset-password/email-subject.txt'

    def get_success_url(self) -> str:
        messages.add_message(
            self.request,
            messages.WARNING,
            "لینک بازنشانی رمز عبور به ایمیل ات ارسال شد.",
        )
        return reverse('account:login')


class ResetPasswordConfirm(auth_views.PasswordResetConfirmView):
    form_class = forms.SetPasswordForm
    template_name = 'account/reset-password/confirm.html'

    def get_success_url(self) -> str:
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "رمز عبورت با موفقیت بازنشانی شد. الان میتونی وارد حسابت شی.",
        )
        return reverse('account:login')
