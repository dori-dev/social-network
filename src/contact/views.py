from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_protect
from utils.mixins import AjaxRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from . import models

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


class UserDetail(generic.DetailView):
    queryset = UserModel.objects.filter(
        is_active=True,
    )
    template_name = 'contact/detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    context_object_name = 'user'


@method_decorator(csrf_protect, name='dispatch')
class FollowUser(LoginRequiredMixin, AjaxRequiredMixin, generic.UpdateView):
    http_method_names = [
        'post',
    ]
    model = UserModel
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action')
        if action:
            try:
                user = self.get_object()
                if action == 'follow':
                    models.Contact.objects.get_or_create(
                        user_from=request.user,
                        user_to=user,
                    )
                else:
                    contact_object = models.Contact.objects.filter(
                        user_from=request.user,
                        user_to=user,
                    )
                    if contact_object.exists():
                        contact_object.delete()
                return JsonResponse(
                    {
                        'status': 'OK',
                    }
                )
            except Exception as err:
                print(err)
                pass
        return JsonResponse(
            {
                'status': 'ERROR',
            }
        )
