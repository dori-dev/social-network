from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserList(LoginRequiredMixin, generic.ListView):
    queryset = UserModel.objects.filter(
        is_active=True,
    )
    context_object_name = 'users'
    paginate_by = 24

    def get_template_names(self):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return 'contact/add-users.html'
        return 'contact/list.html'
