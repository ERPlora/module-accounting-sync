from django.urls import path
from . import views

app_name = 'accounting_sync'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Navigation tab aliases
    path('connections/', views.accounting_connections_list, name='connections'),
    path('log/', views.sync_logs_list, name='log'),


    # AccountingConnection
    path('accounting_connections/', views.accounting_connections_list, name='accounting_connections_list'),
    path('accounting_connections/add/', views.accounting_connection_add, name='accounting_connection_add'),
    path('accounting_connections/<uuid:pk>/edit/', views.accounting_connection_edit, name='accounting_connection_edit'),
    path('accounting_connections/<uuid:pk>/delete/', views.accounting_connection_delete, name='accounting_connection_delete'),
    path('accounting_connections/bulk/', views.accounting_connections_bulk_action, name='accounting_connections_bulk_action'),

    # SyncLog
    path('sync_logs/', views.sync_logs_list, name='sync_logs_list'),
    path('sync_logs/add/', views.sync_log_add, name='sync_log_add'),
    path('sync_logs/<uuid:pk>/edit/', views.sync_log_edit, name='sync_log_edit'),
    path('sync_logs/<uuid:pk>/delete/', views.sync_log_delete, name='sync_log_delete'),
    path('sync_logs/bulk/', views.sync_logs_bulk_action, name='sync_logs_bulk_action'),

    # Settings
    path('settings/', views.settings_view, name='settings'),
]
