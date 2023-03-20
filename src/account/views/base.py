from django.views import generic

from utils.mixins import ViewCounterMixin


class FormView(ViewCounterMixin, generic.FormView):
    form_class = None

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = self.form_class()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        return self.form_invalid(form, **kwargs)

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        context['next'] = self.request.POST.get('next')
        return self.render_to_response(context)
