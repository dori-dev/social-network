from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from utils.mixins import AjaxRequiredMixin
from . import models


class ActionList(AjaxRequiredMixin, generic.ListView):
    context_object_name = 'actions'
    template_name = 'action/add-actions.html'
    paginate_by = 12

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return models.Action.objects.all()
        actions = models.Action.objects.exclude(
            user=self.request.user,
        )
        following = self.request.user.following
        if following.exists():
            following_users = following.distinct().values_list(
                'id', flat=True
            )
            actions = actions.filter(
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
    action_count = 18

    def get_queryset(self):
        actions = models.Action.objects.all()[:self.action_count]
        actions = actions.select_related(
            'user',
            'user__profile',
        ).prefetch_related(
            'target',
        )
        return actions
