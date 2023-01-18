import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from . import models


def create_action(user, verb, target=None):
    now = timezone.now()
    last_hour = now - datetime.timedelta(hours=1)
    similar_actions = models.Action.objects.filter(
        user=user,
        verb=verb,
        created__gte=last_hour,
    )
    if target is not None:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct,
            target_id=target.id,
        )
    if not similar_actions.exists():
        action = models.Action(
            user=user,
            verb=verb,
            target=target,
        )
        action.save()
        return True
    return False


def remove_action(user, verb, target=None):
    actions = models.Action.objects.filter(
        user=user,
        verb=verb,
    )
    if target is not None:
        target_ct = ContentType.objects.get_for_model(target)
        actions.filter(
            target_ct=target_ct,
            target_id=target.id,
        )
    if actions.exists():
        actions.delete()
