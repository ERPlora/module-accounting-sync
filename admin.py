from django.contrib import admin

from .models import AccountingConnection, SyncLog

@admin.register(AccountingConnection)
class AccountingConnectionAdmin(admin.ModelAdmin):
    list_display = ['provider', 'name', 'status', 'access_token', 'refresh_token']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']


@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = ['connection', 'direction', 'entity_type', 'records_synced', 'status']
    readonly_fields = ['id', 'hub_id', 'created_at', 'updated_at']
    ordering = ['-created_at']

