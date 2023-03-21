from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.urls import reverse

from utils.mixins import ViewCounterMixin
from account import forms


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
