
import csv
from django.views import generic
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import get_user_model
from utils.mixins import SuperUserRequireMixin

UserModel = get_user_model()


class UsersExportCSV(SuperUserRequireMixin, generic.ListView):
    queryset = UserModel.objects.filter(
        is_active=True,
    )

    def get(self, request, *args, **kwargs):
        response = HttpResponse(
            content_type="text/csv",
        )
        response['content-disposition'] = 'attachment;filename=users.csv'
        writer = csv.writer(response)
        writer.writerow([
            'User Name',
            'First Name',
            'Email',
            'Birth Date',
            'Profile Photo',
            'Posts Count',
            'Followers',
            'Following',
        ])
        users = self.queryset.select_related(
            'profile',
        ).prefetch_related(
            'following',
            'followers',
            'posts',
        ).annotate(
            total_followers=Count('followers'),
            total_following=Count('following'),
            total_posts=Count('posts'),
        ).distinct().values_list(
            'username',
            'first_name',
            'email',
            'profile__date_of_birth',
            'profile__photo',
            'total_posts',
            'total_followers',
            'total_following',
        )
        for user in users:
            writer.writerow(user)
        return response
