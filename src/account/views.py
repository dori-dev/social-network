from django.shortcuts import render
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth import views as auth_views
from django.contrib.auth import login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse

from action.utils import create_action
from utils.mixins import ViewCounterMixin
from . import forms

User = get_user_model()


class UserLogin(ViewCounterMixin, auth_views.LoginView):
    form_class = forms.LoginForm
    template_name = 'account/login.html'
    redirect_authenticated_user = True

    def get_success_url(self) -> str:
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "با موفقیت وارد حساب ات شدی!",
        )
        username = self.request.user.username
        return reverse('user:detail', args=(username,))


class UserLogout(ViewCounterMixin, auth_views.LogoutView):
    template_name = 'account/logged_out.html'


class Register(ViewCounterMixin, generic.FormView):
    form_class = forms.RegisterForm
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
        next = self.request.POST.get('next')
        if next:
            return redirect(next)
        return redirect('user:detail', username=user.username)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['next'] = self.request.POST.get('next')
        return self.render_to_response(context)


class Edit(ViewCounterMixin, LoginRequiredMixin, generic.View):
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
        profile = profile_form.save(commit=False)
        profile.save()
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "پروفایلت با موفقیت بروزرسانی شد!",
        )
        user = self.request.user
        create_action(
            user,
            'update',
        )
        return redirect('user:detail', username=user.username)

    def form_invalid(self, user_form, profile_form, **kwargs):
        context = {
            'user_form': user_form,
            'profile_form': profile_form,
        }
        return render(self.request, self.template_name, context)


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
