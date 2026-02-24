from django.contrib import admin

from .models import AccountingConnection, SyncLog

@admin.register(AccountingConnection)
class AccountingConnectionAdmin(admin.ModelAdmin):
    list_display = ['provider', 'name', 'status', 'created_at']
    search_fields = ['provider', 'name', 'status', 'access_token']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(SyncLog)
class SyncLogAdmin(admin.ModelAdmin):
    list_display = ['connection', 'direction', 'entity_type', 'records_synced', 'status', 'created_at']
    search_fields = ['direction', 'entity_type', 'status', 'error_message']
    readonly_fields = ['created_at', 'updated_at']

