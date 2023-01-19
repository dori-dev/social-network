from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.translation import gettext as _


def humanize(date_time):
    time = naturaltime(date_time)
    if time in ["now", "الان"]:
        return "الان"
    time = time.\
        replace(",", " and").\
        replace("،", " and ").\
        replace("ago", "")
    time = time.split("and")[0].strip()
    time = f"{time} ago"
    return " ".join(_(word) for word in time.split())
