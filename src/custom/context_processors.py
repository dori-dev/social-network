import datetime
import pytz
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Count, Sum
import redis
import jdatetime
from jalali_date import datetime2jalali
from post.models import Post
from action.models import Action
from contact.models import Contact


r = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
)

UserModel = get_user_model()


def key2path(key: bytes):
    key = key.decode('utf-8')
    return key.split(':')[1]


def date2jdate(datetime) -> datetime.datetime:
    return datetime2jalali(
        datetime
    ).replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone(settings.TIME_ZONE)
    )


def jdate2date(jalali_datetime: jdatetime.datetime) -> datetime.datetime:
    year, month, day = jdatetime.JalaliToGregorian(
        jyear=jalali_datetime.year,
        jmonth=jalali_datetime.month,
        jday=jalali_datetime.day
    ).getGregorianList()
    return datetime.datetime(
        year=year,
        month=month,
        day=day,
    ).replace(tzinfo=pytz.utc).astimezone(
        pytz.timezone(settings.TIME_ZONE)
    )


def date_clear(datetime: datetime.datetime) -> datetime.datetime:
    return datetime.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )


MONTHS = {
    jdatetime.datetime.j_month_fa_to_num(month): month
    for month in jdatetime.datetime.j_months_fa
}


def access_data(request):
    if not request.META['PATH_INFO'] == "/admin/":
        return {}
    now = timezone.now()
    last_month = now - datetime.timedelta(days=30)
    jalali_last_month = date2jdate(last_month)
    users_count = UserModel.objects.count()
    users_last_month = UserModel.objects.filter(
        date_joined__gte=last_month,
    ).count()
    posts_count = Post.objects.count()
    posts_last_month = Post.objects.filter(
        created__gte=jalali_last_month,
    ).count()
    actions_count = Action.objects.count()
    actions_last_month = Action.objects.filter(
        created__gte=last_month,
    ).count()
    contacts = Contact.objects.count()
    contacts_last_month = Contact.objects.filter(
        created__gte=jalali_last_month,
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
    data = {}
    this_month = date_clear(date2jdate(now))
    month_name = MONTHS[this_month.month]
    data[month_name] = Action.objects.filter(
        created__gte=jdate2date(date_clear(date2jdate(now))),
        created__lte=now,
    ).count()
    first_month = this_month
    for amount in range(1, 5):
        if first_month.month - amount > 0:
            second_month = first_month.replace(
                month=first_month.month - amount,
            )
            print('a')
        else:
            amount = first_month.month - amount
            second_month = first_month.replace(
                month=(12 + amount),
                year=first_month.year - 1,
            )
            print('b')
        second_month = date_clear(second_month)
        print(second_month)
        actions = Action.objects.filter(
            created__gte=jdate2date(second_month),
            created__lt=jdate2date(first_month),
        )
        month_name = MONTHS[second_month.month]
        data[month_name] = actions.count()
    data = {
        key: value
        for key, value in reversed(data.items())
    }
    keys = list(data.keys())
    keys.append('')
    values = list(data.values())
    values.insert(0, 0)
    data = dict(zip(keys, values))
    return {
        'users_count': users_count,
        'users_last_month': users_last_month,
        'posts_count': posts_count,
        'posts_last_month': posts_last_month,
        'contacts_count': contacts,
        'contacts_last_month': contacts_last_month,
        'actions_count': actions_count,
        'actions_last_month': actions_last_month,
        'path_views': path_views,
        'staff_users': staff_users,
        'top_users': top_users_data,
        'actions_data': data,
    }
