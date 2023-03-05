import datetime
import pytz

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings
from django.db.models import Count, Sum
from django.urls import reverse
from django.contrib.admin.models import LogEntry
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


MONTHS = {
    jdatetime.datetime.j_month_fa_to_num(month): month
    for month in jdatetime.datetime.j_months_fa
}

WEEK_DAYS = {
    0: 'دوشنبه',
    1: 'سه شنبه',
    2: 'چهار شنبه',
    3: 'پنج شنبه',
    4: 'جمعه',
    5: 'شنبه',
    6: 'یک شنبه',
}

JALALI_WEEK_DAYS = {
    0: 'شنبه',
    1: 'یک شنبه',
    2: 'دوشنبه',
    3: 'سه شنبه',
    4: 'چهار شنبه',
    5: 'پنج شنبه',
    6: 'جمعه',
}

TOP_USERS_COUNT = 12


def date2jdate(datetime) -> datetime.datetime:
    return timezone.make_aware(
        datetime2jalali(datetime),
        pytz.timezone(settings.TIME_ZONE)
    )


def jdate2date(jalali_datetime: jdatetime.datetime) -> datetime.datetime:
    year, month, day = jdatetime.JalaliToGregorian(
        jyear=jalali_datetime.year,
        jmonth=jalali_datetime.month,
        jday=jalali_datetime.day
    ).getGregorianList()
    return timezone.make_aware(
        datetime.datetime(
            year=year,
            month=month,
            day=day,
        ),
        pytz.timezone(settings.TIME_ZONE)
    )


def clear_data(datetime: datetime.datetime, day=True) -> datetime.datetime:
    datetime = datetime.replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )
    if day:
        return datetime.replace(day=1)
    return datetime


def get_last_week_info(model, now):
    field_name = 'created'
    week_days = WEEK_DAYS
    if model == UserModel:
        field_name = 'date_joined'
    if model in (Post, Contact):
        now = date2jdate(now)
        week_days = JALALI_WEEK_DAYS
    data = {}
    today = clear_data(now, False)
    one_day = datetime.timedelta(days=1)
    day_name = week_days[today.weekday()]
    data[day_name] = model.objects.filter(**{
        f"{field_name}__gte": today,
        f"{field_name}__lte": now,
    }).count()
    first_day = today
    for _ in range(1, 7):
        second_day = first_day - one_day
        second_day = clear_data(second_day, False)
        day_name = week_days[second_day.weekday()]
        data[day_name] = model.objects.filter(**{
            f"{field_name}__gte": second_day,
            f"{field_name}__lt": first_day,
        }).count()
        first_day = second_day
    return data


def format_data(data: dict):
    data = {
        key: value
        for key, value in reversed(data.items())
    }
    keys = list(data.keys())
    keys.append('')
    values = list(data.values())
    values.insert(0, 0)
    return dict(zip(keys, values))


def calc_objects_count(now: datetime.datetime) -> dict:
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
    return {
        'users_count': users_count,
        'users_last_month': users_last_month,
        'posts_count': posts_count,
        'posts_last_month': posts_last_month,
        'contacts_count': contacts,
        'contacts_last_month': contacts_last_month,
        'actions_count': actions_count,
        'actions_last_month': actions_last_month,
    }


def get_top_users() -> dict:
    top_users = UserModel.objects.annotate(
        total_followers=Count('followers_set', distinct=True)
    ).annotate(
        total_posts=Count('posts', distinct=True),
    ).annotate(
        total_posts_likes=Sum('posts__total_likes', distinct=True),
    ).order_by(
        '-total_followers',
        '-total_posts_likes',
    )
    top_users_data = list(top_users.values_list(
        'username',
        'total_followers',
        'total_posts',
        'total_posts_likes',
    )[:TOP_USERS_COUNT])
    top_users_data = {
        item[0]: list(item[1:]) for item in top_users_data
    }
    return top_users_data


def get_actions_data(now: datetime.datetime) -> dict:
    data = {}
    this_month = clear_data(date2jdate(now))
    month_name = MONTHS[this_month.month]
    data[month_name] = Action.objects.filter(
        created__gte=jdate2date(clear_data(date2jdate(now))),
        created__lte=now,
    ).count()
    first_month = this_month
    for _ in range(1, 5):
        if first_month.month - 1 > 0:
            second_month = first_month.replace(
                month=first_month.month - 1,
            )
        else:
            second_month = first_month.replace(
                month=12,
                year=first_month.year - 1,
            )
        second_month = clear_data(second_month)
        actions = Action.objects.filter(
            created__gte=jdate2date(second_month),
            created__lt=jdate2date(first_month),
        )
        month_name = MONTHS[second_month.month]
        data[month_name] = actions.count()
        first_month = second_month
    data = format_data(data)
    return data


def get_chart_data(now: datetime.datetime) -> dict:
    return {
        'actions_data': get_actions_data(now),
        'actions_data_week': format_data(get_last_week_info(Action, now)),
        'posts_data': get_last_week_info(Post, now),
        'contacts_data': get_last_week_info(Contact, now),
        'users_data': get_last_week_info(UserModel, now),
    }


def key2path(key: bytes):
    key = key.decode('utf-8')
    return key.split(':')[1]


def get_visits_count() -> list:
    return [
        (key2path(key), r.scard(key))
        for key in r.keys('page:*')
    ]


def get_managers():
    return UserModel.objects.filter(
        is_staff=True,
    )


def last_10_logentry():
    return LogEntry.objects.all()[:10]


def access_data(request):
    if not request.META['PATH_INFO'] == reverse('admin:index'):
        return {}
    now = timezone.now()
    return {
        **calc_objects_count(now),
        'path_views': get_visits_count(),
        'staff_users': get_managers(),
        "top_users": get_top_users(),
        **get_chart_data(now),
        'logentry': last_10_logentry(),
    }
