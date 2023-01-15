from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserList(LoginRequiredMixin, generic.ListView):
    queryset = UserModel.objects.filter(
        is_active=True,
    )
    template_name = 'contact/list.html'
    context_object_name = 'users'
    paginate_by = 24
