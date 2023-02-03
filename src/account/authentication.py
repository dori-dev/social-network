from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from social_core.backends.google import GoogleOAuth2
from social_core.exceptions import AuthAlreadyAssociated

User = get_user_model()


class EmailAuthBackend:
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def user_can_authenticate(self, user):
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        return user if self.user_can_authenticate(user) else None


class CustomGoogleOAuth2(GoogleOAuth2):
    def pipeline(self, pipeline, pipeline_index=0, *args, **kwargs):
        try:
            return super().pipeline(pipeline, pipeline_index, *args, **kwargs)
        except IntegrityError:
            email = kwargs['response']['email']
            user = User.objects.get(email=email)
            user.social_user = None
            user.is_new = False
            return user
        except AuthAlreadyAssociated:
            return None
