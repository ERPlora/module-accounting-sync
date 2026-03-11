"""
AI context for the Accounting Sync module.
Loaded into the assistant system prompt when this module's tools are active.
"""

CONTEXT = """
## Module Knowledge: Accounting Sync

### Models

**AccountingConnection**
- `provider` (CharField, max 30): external accounting software identifier (e.g. `quickbooks`, `xero`, `sage`)
- `name` (CharField): human-readable connection name
- `status` (CharField, default `disconnected`): `disconnected`, `connected`, `error`
- `access_token` / `refresh_token` (TextField): OAuth tokens for the external provider
- `last_sync_at` (DateTimeField, nullable): timestamp of most recent sync
- `sync_enabled` (bool, default False): whether automatic sync is active
- Related: `logs` (SyncLog set)

**SyncLog**
- `connection` (FK AccountingConnection): which connection this log belongs to
- `direction` (CharField, default `push`): `push` (Hub → provider) or `pull` (provider → Hub)
- `entity_type` (CharField, max 50): what was synced, e.g. `invoices`, `expenses`, `payments`
- `records_synced` (PositiveIntegerField, default 0): count of records processed
- `status` (CharField, default `success`): `success`, `partial`, `error`
- `error_message` (TextField, optional): details when status is `error`

### Key flows

**Connect an external accounting provider:**
1. Create `AccountingConnection` with `provider` and `name`
2. Complete OAuth flow → store `access_token` and `refresh_token`
3. Set `status='connected'` and `sync_enabled=True`

**Review sync history:**
- Query `SyncLog.objects.filter(connection=conn).order_by('-created_at')`
- Check `status` and `error_message` for failed syncs

### Relationships
- AccountingConnection → SyncLog (one-to-many, related_name `logs`)
- No direct FK to invoicing or expenses — sync logic reads those models separately
"""
