from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostList.as_view(), name='list'),
    path('create/', views.CreatePost.as_view(), name='create'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='detail'),
    path('<slug:slug>/like/', views.LikePost.as_view(), name='like'),
]
