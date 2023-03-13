from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse

from action.utils import create_action, remove_action
from utils.mixins import (
    AjaxRequiredMixin,
    PostViewCounterMixin,
    ViewCounterMixin,
)
from . import forms
from comment.forms import CommentCreateForm
from comment.models import Comment
from . import models


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


class PostDetail(
        AccessMixin,
        PostViewCounterMixin,
        generic.DetailView,
        generic.CreateView):
    model = models.Post
    queryset = models.Post.objects.select_related(
        'user',
        'user__profile',
    ).prefetch_related(
        'users_like',
        'users_like__profile',
        'comments',
        'comments__user',
        'comments__replies',
        'comments__replies__user',
    )
    template_name = 'post/detail.html'
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        form = self.form_class(request.POST)
        comment_id = request.POST.get('comment_id')
        if comment_id:
            self.reply_comment(request, form, comment_id)
        self.send_comment(request, form)
        return redirect(self.get_object().get_absolute_url())

    def send_comment(self, request, form, commit=True):
        if form.is_valid():
            new_comment: Comment = form.save(commit=False)
            new_comment.user = request.user
            new_comment.post = self.get_object()
            if commit:
                new_comment.save()
            return new_comment

    def reply_comment(self, request, form, comment_id: int):
        comment = Comment.objects.filter(
            pk=comment_id,
        )
        if comment.exists():
            new_comment = self.send_comment(request, form, commit=False)
            new_comment.reply = comment.first()
            new_comment.is_reply = True
            new_comment.save()


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
        post = form.save(commit=False)
        post.save()
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


class PostList(ViewCounterMixin, generic.ListView):
    model = models.Post
    queryset = models.Post.objects.values(
        'total_likes',
        'image',
        'slug',
    )
    context_object_name = 'posts'
    paginate_by = 24

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return 'post/add-posts.html'
        return 'post/list.html'
