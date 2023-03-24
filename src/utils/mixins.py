from django.shortcuts import redirect
from django.http import HttpResponseBadRequest
from django.http import HttpRequest
from django.contrib import messages
from django.utils.translation import gettext_lazy as _

from account.models import OTP
from config.settings import r


class AjaxRequiredMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseBadRequest()


class SuperUserRequireMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseBadRequest()


class PostViewCounterMixin:
    def get_context_data(self, **kwargs):
        request: HttpRequest = self.request
        context = super().get_context_data(**kwargs)
        x_forwarded_for: str = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        slug = context['post'].slug
        r.sadd(
            f'post:{slug}:view_ips',
            ip_address,
        )
        context["total_views"] = r.scard(f'post:{slug}:view_ips')
        return context


class ViewCounterMixin:
    def dispatch(self, request: HttpRequest, *args, **kwargs):
        x_forwarded_for: str = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        path = request.path
        r.sadd(
            f'page:{path}:view_ips',
            ip_address,
        )
        return super().dispatch(request, *args, **kwargs)


class PhoneRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        phone = request.session.get('phone_number')
        if phone is None:
            messages.error(
                self.request,
                _('First apply to get the verification code.'),
                extra_tags='danger',
            )
            return redirect('account:otp_auth')
        if request.method == 'POST':
            otp = OTP.objects.filter(phone=phone)
            if not otp.exists():
                messages.error(
                    self.request,
                    _('First apply to get the verification code.'),
                    extra_tags='danger',
                )
                return redirect('account:otp_auth')
            self.otp_obj = otp.first()
        return super().dispatch(request, *args, **kwargs)
