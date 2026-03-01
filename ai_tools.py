"""AI tools for the Accounting Sync module."""
from assistant.tools import AssistantTool, register_tool


@register_tool
class ListAccountingConnections(AssistantTool):
    name = "list_accounting_connections"
    description = "List accounting integrations (Xero, QuickBooks, Sage)."
    module_id = "accounting_sync"
    required_permission = "accounting_sync.view_accountingconnection"
    parameters = {"type": "object", "properties": {"status": {"type": "string", "description": "connected, disconnected, error"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from accounting_sync.models import AccountingConnection
        qs = AccountingConnection.objects.all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        return {"connections": [{"id": str(c.id), "provider": c.provider, "name": c.name, "status": c.status, "sync_enabled": c.sync_enabled, "last_sync_at": c.last_sync_at.isoformat() if c.last_sync_at else None} for c in qs]}


@register_tool
class ListSyncLogs(AssistantTool):
    name = "list_sync_logs"
    description = "List accounting sync logs."
    module_id = "accounting_sync"
    required_permission = "accounting_sync.view_synclog"
    parameters = {"type": "object", "properties": {"status": {"type": "string"}, "connection_id": {"type": "string"}, "limit": {"type": "integer"}}, "required": [], "additionalProperties": False}

    def execute(self, args, request):
        from accounting_sync.models import SyncLog
        qs = SyncLog.objects.select_related('connection').all()
        if args.get('status'):
            qs = qs.filter(status=args['status'])
        if args.get('connection_id'):
            qs = qs.filter(connection_id=args['connection_id'])
        limit = args.get('limit', 20)
        return {"logs": [{"id": str(l.id), "connection": l.connection.name if l.connection else None, "direction": l.direction, "entity_type": l.entity_type, "records_synced": l.records_synced, "status": l.status, "error_message": l.error_message, "created_at": l.created_at.isoformat()} for l in qs.order_by('-created_at')[:limit]]}
