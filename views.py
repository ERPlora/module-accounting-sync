"""
Accounting Sync (Xero/QB) Module Views
"""
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.accounts.decorators import login_required
from apps.core.htmx import htmx_view
from apps.modules_runtime.navigation import with_module_nav


@login_required
@with_module_nav('accounting_sync', 'dashboard')
@htmx_view('accounting_sync/pages/dashboard.html', 'accounting_sync/partials/dashboard_content.html')
def dashboard(request):
    """Dashboard view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('accounting_sync', 'connections')
@htmx_view('accounting_sync/pages/connections.html', 'accounting_sync/partials/connections_content.html')
def connections(request):
    """Connections view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('accounting_sync', 'log')
@htmx_view('accounting_sync/pages/log.html', 'accounting_sync/partials/log_content.html')
def log(request):
    """Sync Log view."""
    hub_id = request.session.get('hub_id')
    return {}


@login_required
@with_module_nav('accounting_sync', 'settings')
@htmx_view('accounting_sync/pages/settings.html', 'accounting_sync/partials/settings_content.html')
def settings(request):
    """Settings view."""
    hub_id = request.session.get('hub_id')
    return {}

