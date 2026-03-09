# Accounting Sync (Xero/QB)

## Overview

| Property | Value |
|----------|-------|
| **Module ID** | `accounting_sync` |
| **Version** | `1.0.0` |
| **Icon** | `sync-outline` |
| **Dependencies** | None |

## Models

### `AccountingConnection`

AccountingConnection(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, provider, name, status, access_token, refresh_token, last_sync_at, sync_enabled)

| Field | Type | Details |
|-------|------|---------|
| `provider` | CharField | max_length=30 |
| `name` | CharField | max_length=255 |
| `status` | CharField | max_length=20 |
| `access_token` | TextField | optional |
| `refresh_token` | TextField | optional |
| `last_sync_at` | DateTimeField | optional |
| `sync_enabled` | BooleanField |  |

### `SyncLog`

SyncLog(id, hub_id, created_at, updated_at, created_by, updated_by, is_deleted, deleted_at, connection, direction, entity_type, records_synced, status, error_message)

| Field | Type | Details |
|-------|------|---------|
| `connection` | ForeignKey | → `accounting_sync.AccountingConnection`, on_delete=CASCADE |
| `direction` | CharField | max_length=10 |
| `entity_type` | CharField | max_length=50 |
| `records_synced` | PositiveIntegerField |  |
| `status` | CharField | max_length=20 |
| `error_message` | TextField | optional |

## Cross-Module Relationships

| From | Field | To | on_delete | Nullable |
|------|-------|----|-----------|----------|
| `SyncLog` | `connection` | `accounting_sync.AccountingConnection` | CASCADE | No |

## URL Endpoints

Base path: `/m/accounting_sync/`

| Path | Name | Method |
|------|------|--------|
| `(root)` | `dashboard` | GET |
| `connections/` | `connections` | GET |
| `log/` | `log` | GET |
| `accounting_connections/` | `accounting_connections_list` | GET |
| `accounting_connections/add/` | `accounting_connection_add` | GET/POST |
| `accounting_connections/<uuid:pk>/edit/` | `accounting_connection_edit` | GET |
| `accounting_connections/<uuid:pk>/delete/` | `accounting_connection_delete` | GET/POST |
| `accounting_connections/bulk/` | `accounting_connections_bulk_action` | GET/POST |
| `sync_logs/` | `sync_logs_list` | GET |
| `sync_logs/add/` | `sync_log_add` | GET/POST |
| `sync_logs/<uuid:pk>/edit/` | `sync_log_edit` | GET |
| `sync_logs/<uuid:pk>/delete/` | `sync_log_delete` | GET/POST |
| `sync_logs/bulk/` | `sync_logs_bulk_action` | GET/POST |
| `settings/` | `settings` | GET |

## Permissions

| Permission | Description |
|------------|-------------|
| `accounting_sync.view_accountingconnection` | View Accountingconnection |
| `accounting_sync.add_accountingconnection` | Add Accountingconnection |
| `accounting_sync.manage_sync` | Manage Sync |
| `accounting_sync.manage_settings` | Manage Settings |

**Role assignments:**

- **admin**: All permissions
- **manager**: `add_accountingconnection`, `manage_sync`, `view_accountingconnection`
- **employee**: `add_accountingconnection`, `view_accountingconnection`

## Navigation

| View | Icon | ID | Fullpage |
|------|------|----|----------|
| Dashboard | `speedometer-outline` | `dashboard` | No |
| Connections | `sync-outline` | `connections` | No |
| Sync Log | `list-outline` | `log` | No |
| Settings | `settings-outline` | `settings` | No |

## AI Tools

Tools available for the AI assistant:

### `list_accounting_connections`

List accounting integrations (Xero, QuickBooks, Sage).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | connected, disconnected, error |

### `list_sync_logs`

List accounting sync logs.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No |  |
| `connection_id` | string | No |  |
| `limit` | integer | No |  |

### `toggle_accounting_sync`

Enable or disable sync for an accounting connection.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `connection_id` | string | Yes | Connection ID |
| `enabled` | boolean | Yes | Enable (true) or disable (false) sync |

### `trigger_accounting_sync`

Manually trigger a sync for an accounting connection.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `connection_id` | string | Yes | Connection ID |
| `direction` | string | No | push or pull (default: push) |
| `entity_type` | string | No | Entity to sync: invoices, payments, customers |

## File Structure

```
README.md
__init__.py
admin.py
ai_tools.py
apps.py
forms.py
locale/
  en/
    LC_MESSAGES/
      django.po
  es/
    LC_MESSAGES/
      django.po
migrations/
  0001_initial.py
  __init__.py
models.py
module.py
static/
  accounting_sync/
    css/
    js/
  icons/
    icon.svg
templates/
  accounting_sync/
    pages/
      accounting_connection_add.html
      accounting_connection_edit.html
      accounting_connections.html
      connections.html
      dashboard.html
      index.html
      log.html
      settings.html
      sync_log_add.html
      sync_log_edit.html
      sync_logs.html
    partials/
      accounting_connection_add_content.html
      accounting_connection_edit_content.html
      accounting_connections_content.html
      accounting_connections_list.html
      connections_content.html
      dashboard_content.html
      log_content.html
      panel_accounting_connection_add.html
      panel_accounting_connection_edit.html
      panel_sync_log_add.html
      panel_sync_log_edit.html
      settings_content.html
      sync_log_add_content.html
      sync_log_edit_content.html
      sync_logs_content.html
      sync_logs_list.html
tests/
  __init__.py
  conftest.py
  test_models.py
  test_views.py
urls.py
views.py
```
