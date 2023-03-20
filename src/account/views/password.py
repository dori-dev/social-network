from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

from utils.mixins import ViewCounterMixin
from account import forms


class ChangePassword(
        ViewCounterMixin,
        LoginRequiredMixin,
        auth_views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    template_name = "account/change-password.html"

    def get_success_url(self) -> str:
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "پسورد ات ما موفقیت تغییر کرد.",
        )
        username = self.request.user.username
        return reverse('user:detail', args=(username,))


class ResetPassword(ViewCounterMixin, auth_views.PasswordResetView):
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
        next = self.request.POST.get('next')
        login_page = reverse('account:login')
        if next:
            return f"{login_page}?next={next}"
        return login_page


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
