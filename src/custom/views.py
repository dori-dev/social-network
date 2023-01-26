
import csv
from django.views import generic
from django.http import HttpResponse
from django.db.models import Count
from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utils.mixins import SuperUserRequireMixin

UserModel = get_user_model()


@login_required(login_url="/accounts/login/")
def transaction(request):
    context = {
        'segment': 'transactions'
    }
    return render(request, 'pages/transactions.html', context)


@login_required(login_url="/accounts/login/")
def settings(request):
    context = {
        'segment': 'settings'
    }
    return render(request, 'pages/settings.html', context)


@login_required(login_url="/accounts/login/")
def bs_tables(request):
    context = {
        'parent': 'tables',
        'segment': 'bs_tables',
    }
    return render(request, 'pages/tables/bootstrap-tables.html', context)


@login_required(login_url="/accounts/login/")
def buttons(request):
    context = {
        'parent': 'components',
        'segment': 'buttons',
    }
    return render(request, 'pages/components/buttons.html', context)


@login_required(login_url="/accounts/login/")
def notifications(request):
    context = {
        'parent': 'components',
        'segment': 'notifications',
    }
    return render(request, 'pages/components/notifications.html', context)


@login_required(login_url="/accounts/login/")
def forms(request):
    context = {
        'parent': 'components',
        'segment': 'forms',
    }
    return render(request, 'pages/components/forms.html', context)


@login_required(login_url="/accounts/login/")
def modals(request):
    context = {
        'parent': 'components',
        'segment': 'modals',
    }
    return render(request, 'pages/components/modals.html', context)


@login_required(login_url="/accounts/login/")
def typography(request):
    context = {
        'parent': 'components',
        'segment': 'typography',
    }
    return render(request, 'pages/components/typography.html', context)


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
