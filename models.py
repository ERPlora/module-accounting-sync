from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models.base import HubBaseModel

class AccountingConnection(HubBaseModel):
    provider = models.CharField(max_length=30, verbose_name=_('Provider'))
    name = models.CharField(max_length=255, verbose_name=_('Name'))
    status = models.CharField(max_length=20, default='disconnected', verbose_name=_('Status'))
    access_token = models.TextField(blank=True, verbose_name=_('Access Token'))
    refresh_token = models.TextField(blank=True, verbose_name=_('Refresh Token'))
    last_sync_at = models.DateTimeField(null=True, blank=True, verbose_name=_('Last Sync At'))
    sync_enabled = models.BooleanField(default=False, verbose_name=_('Sync Enabled'))

    class Meta(HubBaseModel.Meta):
        db_table = 'accounting_sync_accountingconnection'

    def __str__(self):
        return self.name


class SyncLog(HubBaseModel):
    connection = models.ForeignKey('AccountingConnection', on_delete=models.CASCADE, related_name='logs')
    direction = models.CharField(max_length=10, default='push', verbose_name=_('Direction'))
    entity_type = models.CharField(max_length=50, verbose_name=_('Entity Type'))
    records_synced = models.PositiveIntegerField(default=0, verbose_name=_('Records Synced'))
    status = models.CharField(max_length=20, default='success', verbose_name=_('Status'))
    error_message = models.TextField(blank=True, verbose_name=_('Error Message'))

    class Meta(HubBaseModel.Meta):
        db_table = 'accounting_sync_synclog'

    def __str__(self):
        return str(self.id)

