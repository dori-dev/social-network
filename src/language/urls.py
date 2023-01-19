from django.urls import path
from . import views

app_name = 'language'

urlpatterns = [
    path('change/', views.change_language, name='change'),
]
