from django import forms
from django.utils.translation import gettext_lazy as _

from .models import AccountingConnection, SyncLog

class AccountingConnectionForm(forms.ModelForm):
    class Meta:
        model = AccountingConnection
        fields = ['provider', 'name', 'status', 'access_token', 'refresh_token', 'last_sync_at', 'sync_enabled']
        widgets = {
            'provider': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'name': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'status': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'access_token': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'refresh_token': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
            'last_sync_at': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'datetime-local'}),
            'sync_enabled': forms.CheckboxInput(attrs={'class': 'toggle'}),
        }

class SyncLogForm(forms.ModelForm):
    class Meta:
        model = SyncLog
        fields = ['connection', 'direction', 'entity_type', 'records_synced', 'status', 'error_message']
        widgets = {
            'connection': forms.Select(attrs={'class': 'select select-sm w-full'}),
            'direction': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'entity_type': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'records_synced': forms.TextInput(attrs={'class': 'input input-sm w-full', 'type': 'number'}),
            'status': forms.TextInput(attrs={'class': 'input input-sm w-full'}),
            'error_message': forms.Textarea(attrs={'class': 'textarea textarea-sm w-full', 'rows': 3}),
        }

