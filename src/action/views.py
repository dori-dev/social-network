from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from utils.mixins import AjaxRequiredMixin
from . import models


class ActionList(LoginRequiredMixin, AjaxRequiredMixin, generic.ListView):
    context_object_name = 'actions'
    template_name = 'action/add-actions.html'
    paginate_by = 24

    def get_queryset(self):
        actions = models.Action.objects.exclude(
            user=self.request.user,
        )
        following = self.request.user.following
        if following.exists():
            following_users = following.distinct().values_list(
                'id', flat=True
            )
            actions.filter(
                user__in=following_users,
            )
        actions = actions.select_related(
            'user',
            'user__profile',
        ).prefetch_related(
            'target',
        )
        return actions


class LastAction(LoginRequiredMixin, generic.ListView):
    context_object_name = 'actions'
    template_name = 'action/actions.html'

    def get_queryset(self):
        actions = models.Action.objects.exclude(
            user=self.request.user,
        )[:10]
        actions = actions.select_related(
            'user',
            'user__profile',
        ).prefetch_related(
            'target',
        )
        return actions
