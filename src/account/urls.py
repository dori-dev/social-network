from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), name='logout'),
    # Change password
    path(
        'change-password/',
        views.ChangePassword.as_view(),
        name='change_password'
    ),
]
