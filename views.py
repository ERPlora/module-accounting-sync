"""
Accounting Sync (Xero/QB) Module Views
"""
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404, render as django_render
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.accounts.decorators import login_required, permission_required
from apps.core.htmx import htmx_view
from apps.core.services import export_to_csv, export_to_excel
from apps.modules_runtime.navigation import with_module_nav

from .models import AccountingConnection, SyncLog

PER_PAGE_CHOICES = [10, 25, 50, 100]


# ======================================================================
# Dashboard
# ======================================================================

@login_required
@with_module_nav('accounting_sync', 'dashboard')
@htmx_view('accounting_sync/pages/index.html', 'accounting_sync/partials/dashboard_content.html')
def dashboard(request):
    hub_id = request.session.get('hub_id')
    return {
        'total_accounting_connections': AccountingConnection.objects.filter(hub_id=hub_id, is_deleted=False).count(),
        'total_sync_logs': SyncLog.objects.filter(hub_id=hub_id, is_deleted=False).count(),
    }


# ======================================================================
# AccountingConnection
# ======================================================================

ACCOUNTING_CONNECTION_SORT_FIELDS = {
    'name': 'name',
    'status': 'status',
    'sync_enabled': 'sync_enabled',
    'provider': 'provider',
    'access_token': 'access_token',
    'refresh_token': 'refresh_token',
    'created_at': 'created_at',
}

def _build_accounting_connections_context(hub_id, per_page=10):
    qs = AccountingConnection.objects.filter(hub_id=hub_id, is_deleted=False).order_by('name')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'accounting_connections': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'name',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_accounting_connections_list(request, hub_id, per_page=10):
    ctx = _build_accounting_connections_context(hub_id, per_page)
    return django_render(request, 'accounting_sync/partials/accounting_connections_list.html', ctx)

@login_required
@with_module_nav('accounting_sync', 'connections')
@htmx_view('accounting_sync/pages/accounting_connections.html', 'accounting_sync/partials/accounting_connections_content.html')
def accounting_connections_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'name')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = AccountingConnection.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(provider__icontains=search_query) | Q(name__icontains=search_query) | Q(status__icontains=search_query) | Q(access_token__icontains=search_query))

    order_by = ACCOUNTING_CONNECTION_SORT_FIELDS.get(sort_field, 'name')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['name', 'status', 'sync_enabled', 'provider', 'access_token', 'refresh_token']
        headers = ['Name', 'Status', 'Sync Enabled', 'Provider', 'Access Token', 'Refresh Token']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='accounting_connections.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='accounting_connections.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'accounting_sync/partials/accounting_connections_list.html', {
            'accounting_connections': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'accounting_connections': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def accounting_connection_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        provider = request.POST.get('provider', '').strip()
        name = request.POST.get('name', '').strip()
        status = request.POST.get('status', '').strip()
        access_token = request.POST.get('access_token', '').strip()
        refresh_token = request.POST.get('refresh_token', '').strip()
        last_sync_at = request.POST.get('last_sync_at') or None
        sync_enabled = request.POST.get('sync_enabled') == 'on'
        obj = AccountingConnection(hub_id=hub_id)
        obj.provider = provider
        obj.name = name
        obj.status = status
        obj.access_token = access_token
        obj.refresh_token = refresh_token
        obj.last_sync_at = last_sync_at
        obj.sync_enabled = sync_enabled
        obj.save()
        return _render_accounting_connections_list(request, hub_id)
    return django_render(request, 'accounting_sync/partials/panel_accounting_connection_add.html', {})

@login_required
def accounting_connection_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(AccountingConnection, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.provider = request.POST.get('provider', '').strip()
        obj.name = request.POST.get('name', '').strip()
        obj.status = request.POST.get('status', '').strip()
        obj.access_token = request.POST.get('access_token', '').strip()
        obj.refresh_token = request.POST.get('refresh_token', '').strip()
        obj.last_sync_at = request.POST.get('last_sync_at') or None
        obj.sync_enabled = request.POST.get('sync_enabled') == 'on'
        obj.save()
        return _render_accounting_connections_list(request, hub_id)
    return django_render(request, 'accounting_sync/partials/panel_accounting_connection_edit.html', {'obj': obj})

@login_required
@require_POST
def accounting_connection_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(AccountingConnection, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_accounting_connections_list(request, hub_id)

@login_required
@require_POST
def accounting_connections_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = AccountingConnection.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_accounting_connections_list(request, hub_id)


# ======================================================================
# SyncLog
# ======================================================================

SYNC_LOG_SORT_FIELDS = {
    'connection': 'connection',
    'status': 'status',
    'records_synced': 'records_synced',
    'direction': 'direction',
    'entity_type': 'entity_type',
    'error_message': 'error_message',
    'created_at': 'created_at',
}

def _build_sync_logs_context(hub_id, per_page=10):
    qs = SyncLog.objects.filter(hub_id=hub_id, is_deleted=False).order_by('connection')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(1)
    return {
        'sync_logs': page_obj,
        'page_obj': page_obj,
        'search_query': '',
        'sort_field': 'connection',
        'sort_dir': 'asc',
        'current_view': 'table',
        'per_page': per_page,
    }

def _render_sync_logs_list(request, hub_id, per_page=10):
    ctx = _build_sync_logs_context(hub_id, per_page)
    return django_render(request, 'accounting_sync/partials/sync_logs_list.html', ctx)

@login_required
@with_module_nav('accounting_sync', 'log')
@htmx_view('accounting_sync/pages/sync_logs.html', 'accounting_sync/partials/sync_logs_content.html')
def sync_logs_list(request):
    hub_id = request.session.get('hub_id')
    search_query = request.GET.get('q', '').strip()
    sort_field = request.GET.get('sort', 'connection')
    sort_dir = request.GET.get('dir', 'asc')
    page_number = request.GET.get('page', 1)
    current_view = request.GET.get('view', 'table')
    per_page = int(request.GET.get('per_page', 10))
    if per_page not in PER_PAGE_CHOICES:
        per_page = 10

    qs = SyncLog.objects.filter(hub_id=hub_id, is_deleted=False)

    if search_query:
        qs = qs.filter(Q(direction__icontains=search_query) | Q(entity_type__icontains=search_query) | Q(status__icontains=search_query) | Q(error_message__icontains=search_query))

    order_by = SYNC_LOG_SORT_FIELDS.get(sort_field, 'connection')
    if sort_dir == 'desc':
        order_by = f'-{order_by}'
    qs = qs.order_by(order_by)

    export_format = request.GET.get('export')
    if export_format in ('csv', 'excel'):
        fields = ['connection', 'status', 'records_synced', 'direction', 'entity_type', 'error_message']
        headers = ['AccountingConnection', 'Status', 'Records Synced', 'Direction', 'Entity Type', 'Error Message']
        if export_format == 'csv':
            return export_to_csv(qs, fields=fields, headers=headers, filename='sync_logs.csv')
        return export_to_excel(qs, fields=fields, headers=headers, filename='sync_logs.xlsx')

    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page_number)

    if request.htmx and request.htmx.target == 'datatable-body':
        return django_render(request, 'accounting_sync/partials/sync_logs_list.html', {
            'sync_logs': page_obj, 'page_obj': page_obj,
            'search_query': search_query, 'sort_field': sort_field,
            'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
        })

    return {
        'sync_logs': page_obj, 'page_obj': page_obj,
        'search_query': search_query, 'sort_field': sort_field,
        'sort_dir': sort_dir, 'current_view': current_view, 'per_page': per_page,
    }

@login_required
def sync_log_add(request):
    hub_id = request.session.get('hub_id')
    if request.method == 'POST':
        direction = request.POST.get('direction', '').strip()
        entity_type = request.POST.get('entity_type', '').strip()
        records_synced = int(request.POST.get('records_synced', 0) or 0)
        status = request.POST.get('status', '').strip()
        error_message = request.POST.get('error_message', '').strip()
        obj = SyncLog(hub_id=hub_id)
        obj.direction = direction
        obj.entity_type = entity_type
        obj.records_synced = records_synced
        obj.status = status
        obj.error_message = error_message
        obj.save()
        return _render_sync_logs_list(request, hub_id)
    return django_render(request, 'accounting_sync/partials/panel_sync_log_add.html', {})

@login_required
def sync_log_edit(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(SyncLog, pk=pk, hub_id=hub_id, is_deleted=False)
    if request.method == 'POST':
        obj.direction = request.POST.get('direction', '').strip()
        obj.entity_type = request.POST.get('entity_type', '').strip()
        obj.records_synced = int(request.POST.get('records_synced', 0) or 0)
        obj.status = request.POST.get('status', '').strip()
        obj.error_message = request.POST.get('error_message', '').strip()
        obj.save()
        return _render_sync_logs_list(request, hub_id)
    return django_render(request, 'accounting_sync/partials/panel_sync_log_edit.html', {'obj': obj})

@login_required
@require_POST
def sync_log_delete(request, pk):
    hub_id = request.session.get('hub_id')
    obj = get_object_or_404(SyncLog, pk=pk, hub_id=hub_id, is_deleted=False)
    obj.is_deleted = True
    obj.deleted_at = timezone.now()
    obj.save(update_fields=['is_deleted', 'deleted_at', 'updated_at'])
    return _render_sync_logs_list(request, hub_id)

@login_required
@require_POST
def sync_logs_bulk_action(request):
    hub_id = request.session.get('hub_id')
    ids = [i.strip() for i in request.POST.get('ids', '').split(',') if i.strip()]
    action = request.POST.get('action', '')
    qs = SyncLog.objects.filter(hub_id=hub_id, is_deleted=False, id__in=ids)
    if action == 'delete':
        qs.update(is_deleted=True, deleted_at=timezone.now())
    return _render_sync_logs_list(request, hub_id)


@login_required
@permission_required('accounting_sync.manage_settings')
@with_module_nav('accounting_sync', 'settings')
@htmx_view('accounting_sync/pages/settings.html', 'accounting_sync/partials/settings_content.html')
def settings_view(request):
    return {}

