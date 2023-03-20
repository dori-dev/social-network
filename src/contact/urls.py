from django.urls import path
from contact.views import list, detail

app_name = 'user'

urlpatterns = [
    path('', list.UserList.as_view(), name='list'),
    path('<str:username>/', detail.UserDetail.as_view(), name='detail'),
    path('<str:username>/follow/', detail.FollowUser.as_view(), name='follow'),
]
