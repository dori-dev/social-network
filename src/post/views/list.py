from django.views import generic

from utils.mixins import ViewCounterMixin
from post import models


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


class PostTagList(generic.ListView):
    model = models.Post
    context_object_name = 'posts'
    paginate_by = 24

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tag"] = self.kwargs.get('slug')
        return context

    def get_queryset(self):
        tag_slug = self.kwargs.get('slug')
        return models.Post.objects.filter(
            tags__slug=tag_slug,
        ).values(
            'total_likes',
            'image',
            'slug',
        )

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return 'post/add-posts.html'
        return 'post/list.html'
