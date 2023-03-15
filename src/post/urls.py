from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('', views.PostList.as_view(), name='list'),
    path('create/', views.CreatePost.as_view(), name='create'),
    path('tag/<slug:slug>/', views.PostTagList.as_view(), name='tag'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='detail'),
    path('<slug:slug>/update/', views.PostUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', views.PostDelete.as_view(), name='delete'),
    path('<slug:slug>/like/', views.LikePost.as_view(), name='like'),
]
