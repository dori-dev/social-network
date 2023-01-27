from django.views import generic
from django.views.decorators.csrf import csrf_protect
from utils.mixins import (
    AjaxRequiredMixin,
    PostViewCounterMixin,
)
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.http import JsonResponse
from action.utils import create_action, remove_action
from . import forms
from . import models


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
            files=request.FILES,
        )
        if form.is_valid():
            return self.form_valid(form, **kwargs)
        return self.form_invalid(form, **kwargs)

    def form_valid(self, form: forms.CreatePostForm, **kwargs):
        post: models.Post = form.save(commit=False)
        post.user = self.request.user
        post.save()
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


class PostDetail(PostViewCounterMixin, generic.DeleteView):
    model = models.Post
    template_name = 'post/detail.html'


@method_decorator(csrf_protect, name='dispatch')
class LikePost(LoginRequiredMixin, AjaxRequiredMixin, generic.UpdateView):
    http_method_names = [
        'post',
    ]
    model = models.Post

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action:
            try:
                post: models.Post = self.get_object()
                if action == 'like':
                    post.users_like.add(request.user)
                    create_action(
                        self.request.user,
                        'like',
                        post,
                    )
                else:
                    post.users_like.remove(request.user)
                    remove_action(
                        self.request.user,
                        'like',
                        post,
                    )
                return JsonResponse(
                    {
                        'status': 'OK',
                    }
                )
            except Exception:
                pass
        return JsonResponse(
            {
                'status': 'ERROR',
            }
        )


class PostList(generic.ListView):
    model = models.Post
    context_object_name = 'posts'
    paginate_by = 24

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return 'post/add-posts.html'
        return 'post/list.html'
