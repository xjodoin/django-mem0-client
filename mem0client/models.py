from django.db import models
import uuid


class MemoryHistory(models.Model):
    """Django model for storing memory history, replacing SQLite storage."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    memory_id = models.CharField(max_length=36)  # UUID in string format
    prev_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    action = models.CharField(max_length=10)
    created_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['memory_id']),
        ]
