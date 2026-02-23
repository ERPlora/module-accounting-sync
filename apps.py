from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountingSyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounting_sync'
    label = 'accounting_sync'
    verbose_name = _('Accounting Sync (Xero/QB)')

    def ready(self):
        pass
