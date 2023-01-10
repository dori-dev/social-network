from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from . import forms


class CreatePost(LoginRequiredMixin, generic.FormView):
    form_class = forms.CreatePostForm
    template_name = 'post/create.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['form'] = forms.CreatePostForm()
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        form: forms.CreatePostForm = forms.CreatePostForm(
            request.POST,
        )
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        return self.form_invalid(form, **kwargs)

    def form_valid(self, form: forms.CreatePostForm, **kwargs):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
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
