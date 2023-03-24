from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages

from utils.mixins import PhoneRequiredMixin
from account import forms, utils, models
from account.views.base import FormView


class OtpAuth(FormView):
    form_class = forms.OtpForm
    template_name = 'account/otp/auth.html'

    def form_valid(self, form, **kwargs):
        phone = form.cleaned_data['phone']
        otp_code = utils.generate_otp()
        utils.send_otp(phone, otp_code)
        self.request.session['phone_number'] = phone
        messages.success(
            self.request,
            'کد تایید با موفقیت ارسال شد.',
        )
        otp_obj, created = models.OTP.objects.get_or_create(phone=phone)
        otp_obj.otp = otp_code
        otp_obj.save()
        if created or otp_obj.user is None:
            return redirect('account:otp_register')
        return redirect('account:otp_login')


class OtpLogin(PhoneRequiredMixin, FormView):
    form_class = forms.OtpLoginForm
    template_name = 'account/otp/login.html'

    def form_valid(self, form: forms.RegisterForm, **kwargs):
        code = form.cleaned_data['otp']
        user = authenticate(
            self.request,
            password=code,
            otp_obj=self.otp_obj,
        )
        if user is not None:
            login(self.request, user)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "با موفقیت وارد حساب ات شدی!",
            )
            self.request.session['phone_number'] = None
            next = self.request.POST.get('next')
            if next:
                return redirect(next)
            return redirect('user:detail', username=user.username)
        return redirect('account:otp_login')


class OtpRegister(PhoneRequiredMixin, FormView):
    form_class = forms.OtpRegisterForm
    template_name = 'account/otp/register.html'

    def form_valid(self, form: forms.OtpRegisterForm, **kwargs):
        code = form.cleaned_data['otp']
        otp_obj = self.otp_obj
        if not otp_obj.user:
            user = form.save(commit=False)
            otp_obj.user = user
        user = authenticate(
            self.request,
            password=code,
            otp_obj=otp_obj,
        )
        if user is not None:
            user.save()
            otp_obj.save()
            login(self.request, user)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                "به سایت <strong>ویزیتور ایکس</strong> خوش اومدی :)",
            )
            self.request.session['phone_number'] = None
            next = self.request.POST.get('next')
            if next:
                return redirect(next)
            return redirect('user:detail', username=user.username)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['next'] = self.request.POST.get('next')
        return self.render_to_response(context)
