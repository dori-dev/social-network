from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('', views.UserList.as_view(), name='list'),
    path('<str:username>/', views.UserDetail.as_view(), name='detail'),
    path('<str:username>/follow/', views.FollowUser.as_view(), name='follow'),
]
