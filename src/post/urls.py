from django.urls import path
from post.views import list, create, detail, update

app_name = 'post'

urlpatterns = [
    path('', list.PostList.as_view(), name='list'),
    path('tag/<slug:slug>/', list.PostTagList.as_view(), name='tag'),
    path('create/', create.CreatePost.as_view(), name='create'),
    path('<slug:slug>/', detail.PostDetail.as_view(), name='detail'),
    path('<slug:slug>/like/', detail.LikePost.as_view(), name='like'),
    path('<slug:slug>/update/', update.PostUpdate.as_view(), name='update'),
    path('<slug:slug>/delete/', update.PostDelete.as_view(), name='delete'),
]
