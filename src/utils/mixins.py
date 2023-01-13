from django.http import HttpResponseBadRequest
from django.core.handlers.wsgi import WSGIRequest


class AjaxRequiredMixin:
    def dispatch(self, request: WSGIRequest, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseBadRequest()
