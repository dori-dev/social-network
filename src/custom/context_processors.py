import datetime
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Count, Sum
from post.models import Post
from action.models import Action
from contact.models import Contact
import redis

r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

UserModel = get_user_model()


def key2path(key: bytes):
    key = key.decode('utf-8')
    return key.split(':')[1]


def access_data(request):
    if not request.META['PATH_INFO'] == "/admin/":
        return {}
    now = timezone.now()
    last_month = now - datetime.timedelta(days=30)
    users_count = UserModel.objects.count()
    users_last_month = UserModel.objects.filter(
        date_joined__gte=last_month,
    ).count()
    posts_count = Post.objects.count()
    posts_last_month = Post.objects.filter(
        created__gte=last_month,
    ).count()
    contacts = Contact.objects.count()
    contacts_last_month = Contact.objects.filter(
        created__gte=last_month,
    ).count()
    path_views = [
        (key2path(key), r.scard(key))
        for key in r.keys('page:*')
    ]
    staff_users = UserModel.objects.filter(
        is_staff=True,
    )
    top_users = UserModel.objects.annotate(
        total_followers=Count('followers_set', distinct=True)
    ).annotate(
        total_posts=Count('posts', distinct=True),
    ).order_by(
        '-total_followers'
    )[:10]
    top_users_data = list(top_users.values_list(
        'username',
        'total_followers',
        'total_posts',
    ))
    top_users_data = {
        item[0]: list(item[1:]) for item in top_users_data
    }
    for user in top_users:
        top_users_data[user.username].append(
            user.posts.aggregate(
                sum=Sum('total_likes'),
            )['sum']
        )
    return {
        'users_count': users_count,
        'users_last_month': users_last_month,
        'posts_count': posts_count,
        'posts_last_month': posts_last_month,
        'contacts_count': contacts,
        'contacts_last_month': contacts_last_month,
        'path_views': path_views,
        'staff_users': staff_users,
        'top_users': top_users_data,
    }
