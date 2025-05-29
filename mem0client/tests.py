from django.test import TestCase
from django.utils import timezone

from .memory_manager import DjangoMemoryManager
from .models import MemoryHistory


class DjangoMemoryManagerTestCase(TestCase):
    def setUp(self):
        self.manager = DjangoMemoryManager()

    def test_add_history_with_new_fields(self):
        """Test adding history with the new schema fields."""
        memory_id = "test-memory-123"
        old_memory = "This is the old memory content"
        new_memory = "This is the new memory content"
        event = "UPDATE"
        actor_id = "user-456"
        role = "admin"
        
        # Add history entry
        self.manager.add_history(
            memory_id=memory_id,
            old_memory=old_memory,
            new_memory=new_memory,
            event=event,
            actor_id=actor_id,
            role=role
        )
        
        # Verify it was saved
        history_entries = MemoryHistory.objects.filter(memory_id=memory_id)
        self.assertEqual(history_entries.count(), 1)
        
        entry = history_entries.first()
        self.assertEqual(entry.memory_id, memory_id)
        self.assertEqual(entry.old_memory, old_memory)
        self.assertEqual(entry.new_memory, new_memory)
        self.assertEqual(entry.event, event)
        self.assertEqual(entry.actor_id, actor_id)
        self.assertEqual(entry.role, role)
        self.assertFalse(entry.is_deleted)

    def test_get_history_returns_correct_format(self):
        """Test that get_history returns data in the correct format."""
        memory_id = "test-memory-456"
        
        # Add a history entry
        self.manager.add_history(
            memory_id=memory_id,
            old_memory=None,
            new_memory="New memory created",
            event="ADD",
            actor_id="user-789",
            role="user"
        )
        
        # Get history
        history = self.manager.get_history(memory_id)
        
        self.assertEqual(len(history), 1)
        entry = history[0]
        
        # Check all expected fields are present
        expected_fields = [
            "id", "memory_id", "old_memory", "new_memory", "event",
            "created_at", "updated_at", "is_deleted", "actor_id", "role"
        ]
        for field in expected_fields:
            self.assertIn(field, entry)
        
        # Check values
        self.assertEqual(entry["memory_id"], memory_id)
        self.assertEqual(entry["old_memory"], None)
        self.assertEqual(entry["new_memory"], "New memory created")
        self.assertEqual(entry["event"], "ADD")
        self.assertEqual(entry["actor_id"], "user-789")
        self.assertEqual(entry["role"], "user")
        self.assertFalse(entry["is_deleted"])

    def test_reset_clears_all_history(self):
        """Test that reset removes all history entries."""
        # Add some test data
        self.manager.add_history(
            memory_id="test-1",
            old_memory=None,
            new_memory="Memory 1",
            event="ADD"
        )
        self.manager.add_history(
            memory_id="test-2",
            old_memory=None,
            new_memory="Memory 2",
            event="ADD"
        )
        
        # Verify data exists
        self.assertEqual(MemoryHistory.objects.count(), 2)
        
        # Reset
        self.manager.reset()
        
        # Verify all data is gone
        self.assertEqual(MemoryHistory.objects.count(), 0)

    def test_optional_parameters_are_optional(self):
        """Test that the new optional parameters can be omitted."""
        memory_id = "test-memory-optional"
        
        # Add history with minimal parameters
        self.manager.add_history(
            memory_id=memory_id,
            old_memory="Old content",
            new_memory="New content",
            event="UPDATE"
        )
        
        # Verify it was saved with None values for optional fields
        entry = MemoryHistory.objects.get(memory_id=memory_id)
        self.assertIsNone(entry.actor_id)
        self.assertIsNone(entry.role)
        self.assertIsNone(entry.created_at)
        self.assertIsNone(entry.updated_at)
