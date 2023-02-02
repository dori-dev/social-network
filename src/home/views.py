from django.views import generic
from post.models import Post

from utils.mixins import ViewCounterMixin


class Home(ViewCounterMixin, generic.ListView):
    queryset = Post.objects.order_by("?")
    context_object_name = 'posts'
    paginate_by = 24

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return 'post/add-posts.html'
        return 'home/index.html'
