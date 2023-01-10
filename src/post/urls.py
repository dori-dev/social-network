from django.urls import path
from . import views

app_name = 'posts'

urlpatterns = [
    path('create/', views.CreatePost.as_view(), name='create'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='detail'),
]
