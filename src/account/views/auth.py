from django.shortcuts import redirect
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse

from utils.mixins import ViewCounterMixin
from account import forms
from account.views.base import FormView


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


class Register(FormView):
    form_class = forms.RegisterForm
    template_name = 'account/register.html'

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
