from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect

from action.utils import create_action
from utils.mixins import ViewCounterMixin
from utils.functions import extract_tags
from post import forms, models


class CreatePost(ViewCounterMixin, LoginRequiredMixin, generic.FormView):
    form_class = forms.CreateUpdatePostFrom
    template_name = 'post/create.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = forms.CreateUpdatePostFrom()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form: forms.CreateUpdatePostFrom = forms.CreateUpdatePostFrom(
            request.POST,
            files=request.FILES,
        )
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        return self.form_invalid(form, **kwargs)

    def form_valid(self, form: forms.CreateUpdatePostFrom, **kwargs):
        post: models.Post = form.save(commit=False)
        tags = extract_tags(post.description)
        post.user = self.request.user
        post.save()
        post.tags.clear()
        post.tags.add(*tags)
        create_action(
            self.request.user,
            'share',
            post,
        )
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "پست ات با موفقیت منتشر شد :)",
        )
        return redirect(post.get_absolute_url())

    def form_invalid(self, form, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return self.render_to_response(context)
