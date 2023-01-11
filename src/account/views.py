from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from . import forms

User = get_user_model()


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
        return self.form_invalid(form, **kwargs)

    def form_valid(self, form: forms.RegisterForm, **kwargs):
        user = form.save()
        login(
            self.request,
            user,
            'django.contrib.auth.backends.ModelBackend',
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


class Edit(LoginRequiredMixin, generic.View):
    success_url = reverse_lazy('account:dashboard')
    template_name = 'account/edit.html'

    def get(self, request, *args, **kwargs):
        context = {
            'user_form': forms.UserEditForm(
                instance=request.user,
            ),
            'profile_form': forms.UserProfileEditForm(
                instance=request.user.profile,
            ),
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user_form = forms.UserEditForm(
            data=request.POST,
            instance=request.user,
        )
        profile_form = forms.UserProfileEditForm(
            data=request.POST,
            instance=request.user.profile,
            files=request.FILES,
        )
        if user_form.is_valid() and profile_form.is_valid():
            return self.form_valid(user_form, profile_form, **kwargs)
        return self.form_invalid(user_form, profile_form, **kwargs)

    def form_valid(self, user_form, profile_form, **kwargs):
        user_form.save()
        profile_form.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "پروفایلت با موفقیت بروزرسانی شد!",
        )
        return redirect(self.success_url)

    def form_invalid(self, user_form, profile_form, **kwargs):
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(self.request, self.template_name, context)


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
