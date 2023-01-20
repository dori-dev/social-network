from django.http import HttpResponseBadRequest
from django.core.handlers.wsgi import WSGIRequest
from django.conf import settings
import redis

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)


class AjaxRequiredMixin:
    def dispatch(self, request: WSGIRequest, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseBadRequest()


class ViewCounterMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = context['post'].slug
        context["total_views"] = r.incr(
            f'post:{slug}:total_views',
            amount=1,
        )
        return context
