from django.shortcuts import redirect
from django.http.request import HttpRequest
from django.utils.translation import activate


def change_language(request: HttpRequest):
    lang = request.GET.get('lang')
    print(lang)
    next = request.GET.get('next')
    activate(lang)
    return redirect(next)
