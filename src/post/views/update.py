from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib import messages
from django.shortcuts import redirect, render

from action.utils import remove_action
from utils.functions import extract_tags
from post import models, forms


class PostUpdate(AccessMixin, generic.View):
    template_name = 'post/update.html'

    def setup(self, request, *args, **kwargs):
        self.object = None
        if request.user.is_authenticated:
            post = request.user.posts.filter(
                slug=kwargs['slug'],
            )
            if post.exists():
                self.object = post.first()
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if self.object is None:
            return redirect(request.user.get_absolute_url())
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {
            'form': forms.CreateUpdatePostFrom(
                instance=self.object,
            ),
            'slug': self.object.slug,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = forms.CreateUpdatePostFrom(
            data=request.POST,
            instance=self.object,
            files=request.FILES,
        )
        if form.is_valid():
            return self.form_valid(form, *args, **kwargs)
        return self.form_invalid(form, *args, **kwargs)

    def form_valid(self, form, *args, **kwargs):
        post: models.Post = form.save(commit=False)
        tags = extract_tags(post.description)
        post.save()
        post.tags.clear()
        post.tags.add(*tags)
        messages.add_message(
            self.request,
            messages.SUCCESS,
            "پست ات با موفقیت بروزرسانی شد!",
        )
        return redirect(post.get_absolute_url())

    def form_invalid(self, form, *args, **kwargs):
        context = {
            'form': form,
            'slug': self.object.slug,
        }
        return render(self.request, self.template_name, context)


class PostDelete(LoginRequiredMixin, generic.View):
    def get(self, request, slug):
        post = request.user.posts.filter(
            slug=slug,
        )
        if post.exists():
            remove_action(
                self.request.user,
                'share',
                post.first(),
            )
            post.delete()
            messages.add_message(
                self.request,
                messages.WARNING,
                "پست ات با موفقیت حذف شد!",
            )
        return redirect(self.request.user.get_absolute_url())
