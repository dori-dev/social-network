from django.urls import path
from custom import views

urlpatterns = [
    # Pages
    path('pages/transaction/', views.transaction, name="transaction"),
    path('pages/settings/', views.settings, name="settings"),
    # Tables
    path('tables/bs-tables/', views.bs_tables, name="bs_tables"),
    # Components
    path('components/buttons/', views.buttons, name="buttons"),
    path('components/notifications/', views.notifications, name="notifications"),
    path('components/forms/', views.forms, name="forms"),
    path('components/modals/', views.modals, name="modals"),
    path('components/typography/', views.typography, name="typography"),
]
