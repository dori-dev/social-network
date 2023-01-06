from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from . import forms


class Dashboard(LoginRequiredMixin, generic.TemplateView):
    template_name = 'account/dashboard.html'


class UserLogin(auth_views.LoginView):
    form_class = forms.LoginForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "با موفقیت وارد حساب ات شدی!",
        )
        return super().get_success_url()


class UserLogout(auth_views.LogoutView):
    template_name = 'account/logged_out.html'


class Register(generic.FormView):
    form_class = forms.RegisterForm
    success_url = reverse_lazy('account:dashboard')
    template_name = 'account/register.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = forms.RegisterForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form: forms.RegisterForm = forms.RegisterForm(request.POST)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        else:
            return self.form_invalid(form, **kwargs)

    def form_valid(self, form: forms.RegisterForm, **kwargs):
        user = form.save()
        login(
            self.request,
            user,
        )
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "به سایت <strong>بگو مگو</strong> خوش اومدی :)",
        )
        return redirect(self.success_url)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)


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
