from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages

from account import forms
from account.views.base import FormView
from account.tokens import account_activation_token
from account import utils


UserModel = get_user_model()


class Register(FormView):
    form_class = forms.RegisterForm
    template_name = 'account/register/register.html'

    def form_valid(self, form: forms.RegisterForm, **kwargs):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی اکانت ویزیتور ایکس'
        message = render_to_string('account/register/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data['email']
        utils.send_mail(mail_subject, message, to_email)
        context = {
            'email': to_email,
        }
        return render(
            self.request,
            'account/register/token_sended.html',
            context
        )


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (
        TypeError,
        ValueError,
        OverflowError,
        UserModel.DoesNotExist
    ):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(
            request,
            user,
            'django.contrib.auth.backends.ModelBackend',
        )
        messages.add_message(
            request,
            messages.SUCCESS,
            "به سایت <strong>ویزیتور ایکس</strong> خوش اومدی :)",
        )
        next = request.POST.get('next')
        if next:
            return redirect(next)
        return redirect('user:detail', username=user.username)
    else:
        return render(request, 'account/register/invalid_token.html')
