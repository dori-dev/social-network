from django.urls import path
from custom import views

urlpatterns = [
    path('users/csv/', views.UsersExportCSV.as_view(), name='users_csv'),
]
