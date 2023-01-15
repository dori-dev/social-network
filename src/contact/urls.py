from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserList.as_view(), name='list'),
]
