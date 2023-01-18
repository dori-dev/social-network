from django.urls import path
from . import views

app_name = 'action'

urlpatterns = [
    path('', views.ActionList.as_view(), name='list'),
]
