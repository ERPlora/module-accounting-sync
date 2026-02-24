"""Tests for accounting_sync views."""
import pytest
from django.urls import reverse


@pytest.mark.django_db
class TestDashboard:
    """Dashboard view tests."""

    def test_dashboard_loads(self, auth_client):
        """Test dashboard page loads."""
        url = reverse('accounting_sync:dashboard')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_dashboard_htmx(self, auth_client):
        """Test dashboard HTMX partial."""
        url = reverse('accounting_sync:dashboard')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_dashboard_requires_auth(self, client):
        """Test dashboard requires authentication."""
        url = reverse('accounting_sync:dashboard')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestAccountingConnectionViews:
    """AccountingConnection view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('accounting_sync:accounting_connections_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('accounting_sync:accounting_connections_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('accounting_sync:accounting_connections_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('accounting_sync:accounting_connections_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('accounting_sync:accounting_connections_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('accounting_sync:accounting_connections_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('accounting_sync:accounting_connection_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('accounting_sync:accounting_connection_add')
        data = {
            'provider': 'New Provider',
            'name': 'New Name',
            'status': 'New Status',
            'access_token': 'Test description',
            'refresh_token': 'Test description',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, accounting_connection):
        """Test edit form loads."""
        url = reverse('accounting_sync:accounting_connection_edit', args=[accounting_connection.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, accounting_connection):
        """Test editing via POST."""
        url = reverse('accounting_sync:accounting_connection_edit', args=[accounting_connection.pk])
        data = {
            'provider': 'Updated Provider',
            'name': 'Updated Name',
            'status': 'Updated Status',
            'access_token': 'Test description',
            'refresh_token': 'Test description',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, accounting_connection):
        """Test soft delete via POST."""
        url = reverse('accounting_sync:accounting_connection_delete', args=[accounting_connection.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        accounting_connection.refresh_from_db()
        assert accounting_connection.is_deleted is True

    def test_bulk_delete(self, auth_client, accounting_connection):
        """Test bulk delete."""
        url = reverse('accounting_sync:accounting_connections_bulk_action')
        response = auth_client.post(url, {'ids': str(accounting_connection.pk), 'action': 'delete'})
        assert response.status_code == 200
        accounting_connection.refresh_from_db()
        assert accounting_connection.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('accounting_sync:accounting_connections_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSyncLogViews:
    """SyncLog view tests."""

    def test_list_loads(self, auth_client):
        """Test list view loads."""
        url = reverse('accounting_sync:sync_logs_list')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_list_htmx(self, auth_client):
        """Test list HTMX partial."""
        url = reverse('accounting_sync:sync_logs_list')
        response = auth_client.get(url, HTTP_HX_REQUEST='true')
        assert response.status_code == 200

    def test_list_search(self, auth_client):
        """Test list search."""
        url = reverse('accounting_sync:sync_logs_list')
        response = auth_client.get(url, {'q': 'test'})
        assert response.status_code == 200

    def test_list_sort(self, auth_client):
        """Test list sorting."""
        url = reverse('accounting_sync:sync_logs_list')
        response = auth_client.get(url, {'sort': 'created_at', 'dir': 'desc'})
        assert response.status_code == 200

    def test_export_csv(self, auth_client):
        """Test CSV export."""
        url = reverse('accounting_sync:sync_logs_list')
        response = auth_client.get(url, {'export': 'csv'})
        assert response.status_code == 200
        assert 'text/csv' in response['Content-Type']

    def test_export_excel(self, auth_client):
        """Test Excel export."""
        url = reverse('accounting_sync:sync_logs_list')
        response = auth_client.get(url, {'export': 'excel'})
        assert response.status_code == 200

    def test_add_form_loads(self, auth_client):
        """Test add form loads."""
        url = reverse('accounting_sync:sync_log_add')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_add_post(self, auth_client):
        """Test creating via POST."""
        url = reverse('accounting_sync:sync_log_add')
        data = {
            'direction': 'New Direction',
            'entity_type': 'New Entity Type',
            'records_synced': '5',
            'status': 'New Status',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_edit_form_loads(self, auth_client, sync_log):
        """Test edit form loads."""
        url = reverse('accounting_sync:sync_log_edit', args=[sync_log.pk])
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_edit_post(self, auth_client, sync_log):
        """Test editing via POST."""
        url = reverse('accounting_sync:sync_log_edit', args=[sync_log.pk])
        data = {
            'direction': 'Updated Direction',
            'entity_type': 'Updated Entity Type',
            'records_synced': '5',
            'status': 'Updated Status',
        }
        response = auth_client.post(url, data)
        assert response.status_code == 200

    def test_delete(self, auth_client, sync_log):
        """Test soft delete via POST."""
        url = reverse('accounting_sync:sync_log_delete', args=[sync_log.pk])
        response = auth_client.post(url)
        assert response.status_code == 200
        sync_log.refresh_from_db()
        assert sync_log.is_deleted is True

    def test_bulk_delete(self, auth_client, sync_log):
        """Test bulk delete."""
        url = reverse('accounting_sync:sync_logs_bulk_action')
        response = auth_client.post(url, {'ids': str(sync_log.pk), 'action': 'delete'})
        assert response.status_code == 200
        sync_log.refresh_from_db()
        assert sync_log.is_deleted is True

    def test_list_requires_auth(self, client):
        """Test list requires authentication."""
        url = reverse('accounting_sync:sync_logs_list')
        response = client.get(url)
        assert response.status_code == 302


@pytest.mark.django_db
class TestSettings:
    """Settings view tests."""

    def test_settings_loads(self, auth_client):
        """Test settings page loads."""
        url = reverse('accounting_sync:settings')
        response = auth_client.get(url)
        assert response.status_code == 200

    def test_settings_requires_auth(self, client):
        """Test settings requires authentication."""
        url = reverse('accounting_sync:settings')
        response = client.get(url)
        assert response.status_code == 302

