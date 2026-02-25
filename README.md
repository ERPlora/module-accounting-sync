# Accounting Sync (Xero/QB) Module

Sync with Xero, QuickBooks and other accounting platforms.

## Features

- Connect to external accounting providers (Xero, QuickBooks)
- OAuth-based connection management with access/refresh tokens
- Bidirectional sync (push and pull) of accounting data
- Sync logging with entity type, record count, and status tracking
- Enable/disable sync per connection
- Last sync timestamp tracking

## Installation

This module is installed automatically via the ERPlora Marketplace.

## Configuration

Access settings via: **Menu > Accounting Sync (Xero/QB) > Settings**

## Usage

Access via: **Menu > Accounting Sync (Xero/QB)**

### Views

| View | URL | Description |
|------|-----|-------------|
| Dashboard | `/m/accounting_sync/dashboard/` | Overview of sync status across connections |
| Connections | `/m/accounting_sync/connections/` | Manage external accounting platform connections |
| Sync Log | `/m/accounting_sync/log/` | View history of sync operations and errors |
| Settings | `/m/accounting_sync/settings/` | Module configuration |

## Models

| Model | Description |
|-------|-------------|
| `AccountingConnection` | External accounting platform connection with provider, status, and OAuth tokens |
| `SyncLog` | Record of a sync operation with direction, entity type, record count, and status |

## Permissions

| Permission | Description |
|------------|-------------|
| `accounting_sync.view_accountingconnection` | View accounting connections |
| `accounting_sync.add_accountingconnection` | Create new connections |
| `accounting_sync.manage_sync` | Trigger and manage sync operations |
| `accounting_sync.manage_settings` | Manage module settings |

## License

MIT

## Author

ERPlora Team - support@erplora.com
