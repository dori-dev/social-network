from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.shortcuts import redirect
from django.http import JsonResponse

from action.utils import create_action, remove_action
from utils.mixins import AjaxRequiredMixin, PostViewCounterMixin
from comment.forms import CommentCreateForm
from comment.models import Comment
from post import models


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
        'related_posts',
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
