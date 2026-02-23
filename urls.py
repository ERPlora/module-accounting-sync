from django.urls import path
from . import views

app_name = 'accounting_sync'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('connections/', views.connections, name='connections'),
    path('log/', views.log, name='log'),
    path('settings/', views.settings, name='settings'),
]
