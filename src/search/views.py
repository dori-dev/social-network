from django.views import generic

from . import forms
from post.models import Post


class SearchView(generic.ListView):
    form_class = forms.SearchForm
    model = Post
    context_object_name = 'posts'
    paginate_by = 24

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('search')
        if query:
            queryset = queryset.filter(
                description__contains=query,
            )
        return queryset

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return 'post/add-posts.html'
        return 'post/list.html'
