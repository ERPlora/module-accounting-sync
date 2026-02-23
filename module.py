from django.utils.translation import gettext_lazy as _

MODULE_ID = 'accounting_sync'
MODULE_NAME = _('Accounting Sync (Xero/QB)')
MODULE_VERSION = '1.0.0'
MODULE_ICON = 'sync-outline'
MODULE_DESCRIPTION = _('Sync with Xero, QuickBooks and other accounting platforms')
MODULE_AUTHOR = 'ERPlora'
MODULE_CATEGORY = 'integrations'

MENU = {
    'label': _('Accounting Sync (Xero/QB)'),
    'icon': 'sync-outline',
    'order': 87,
}

NAVIGATION = [
    {'label': _('Dashboard'), 'icon': 'speedometer-outline', 'id': 'dashboard'},
{'label': _('Connections'), 'icon': 'sync-outline', 'id': 'connections'},
{'label': _('Sync Log'), 'icon': 'list-outline', 'id': 'log'},
{'label': _('Settings'), 'icon': 'settings-outline', 'id': 'settings'},
]

DEPENDENCIES = []

PERMISSIONS = [
    'accounting_sync.view_accountingconnection',
'accounting_sync.add_accountingconnection',
'accounting_sync.manage_sync',
'accounting_sync.manage_settings',
]
