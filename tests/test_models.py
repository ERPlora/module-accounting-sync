"""Tests for accounting_sync models."""
import pytest
from django.utils import timezone

from accounting_sync.models import AccountingConnection, SyncLog


@pytest.mark.django_db
class TestAccountingConnection:
    """AccountingConnection model tests."""

    def test_create(self, accounting_connection):
        """Test AccountingConnection creation."""
        assert accounting_connection.pk is not None
        assert accounting_connection.is_deleted is False

    def test_str(self, accounting_connection):
        """Test string representation."""
        assert str(accounting_connection) is not None
        assert len(str(accounting_connection)) > 0

    def test_soft_delete(self, accounting_connection):
        """Test soft delete."""
        pk = accounting_connection.pk
        accounting_connection.is_deleted = True
        accounting_connection.deleted_at = timezone.now()
        accounting_connection.save()
        assert not AccountingConnection.objects.filter(pk=pk).exists()
        assert AccountingConnection.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, accounting_connection):
        """Test default queryset excludes deleted."""
        accounting_connection.is_deleted = True
        accounting_connection.deleted_at = timezone.now()
        accounting_connection.save()
        assert AccountingConnection.objects.filter(hub_id=hub_id).count() == 0


@pytest.mark.django_db
class TestSyncLog:
    """SyncLog model tests."""

    def test_create(self, sync_log):
        """Test SyncLog creation."""
        assert sync_log.pk is not None
        assert sync_log.is_deleted is False

    def test_soft_delete(self, sync_log):
        """Test soft delete."""
        pk = sync_log.pk
        sync_log.is_deleted = True
        sync_log.deleted_at = timezone.now()
        sync_log.save()
        assert not SyncLog.objects.filter(pk=pk).exists()
        assert SyncLog.all_objects.filter(pk=pk).exists()

    def test_queryset_excludes_deleted(self, hub_id, sync_log):
        """Test default queryset excludes deleted."""
        sync_log.is_deleted = True
        sync_log.deleted_at = timezone.now()
        sync_log.save()
        assert SyncLog.objects.filter(hub_id=hub_id).count() == 0


