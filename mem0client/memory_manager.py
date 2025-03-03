import logging

from .models import MemoryHistory

logger = logging.getLogger(__name__)

class DjangoMemoryManager:
    """
    Django-based implementation to replace SQLiteManager for storing memory history.
    """

    def __init__(self, config_path=None):
        """
        Initialize the Django Memory Manager.
        The config_path parameter is kept for compatibility but isn't used.
        """
        pass

    def add_history(self, memory_id, prev_value, new_value, action, created_at=None, updated_at=None, is_deleted=0):
        """
        Add a history entry for a memory.

        Args:
            memory_id (str): ID of the memory.
            prev_value (str): Previous value of the memory.
            new_value (str): New value of the memory.
            action (str): Action performed on the memory (ADD, UPDATE, DELETE).
            created_at (str, optional): Creation timestamp. Defaults to None.
            updated_at (str, optional): Update timestamp. Defaults to None.
            is_deleted (int, optional): Whether the memory is deleted. Defaults to 0.
        """
        # Create the history entry in the Django model
        MemoryHistory.objects.create(
            memory_id=memory_id,
            prev_value=prev_value,
            new_value=new_value,
            action=action,
            created_at=created_at,
            updated_at=updated_at,
            is_deleted=bool(is_deleted)
        )

        logger.info(f"Added history for memory {memory_id} with action {action}")

    def get_history(self, memory_id):
        """
        Get the history for a memory.

        Args:
            memory_id (str): ID of the memory.

        Returns:
            list: List of history entries for the memory.
        """
        history_entries = MemoryHistory.objects.filter(
            memory_id=memory_id
        ).order_by('created_at')

        # Convert Django model instances to dictionaries
        result = []
        for entry in history_entries:
            history_dict = {
                "memory_id": entry.memory_id,
                "action": entry.action,
            }

            if entry.prev_value:
                history_dict["prev_value"] = entry.prev_value

            if entry.new_value:
                history_dict["new_value"] = entry.new_value

            if entry.created_at:
                history_dict["created_at"] = entry.created_at.isoformat()

            if entry.updated_at:
                history_dict["updated_at"] = entry.updated_at.isoformat()

            history_dict["is_deleted"] = 1 if entry.is_deleted else 0

            result.append(history_dict)

        return result

    def reset(self):
        """
        Reset the history store.
        """
        MemoryHistory.objects.all().delete()
        logger.warning("Reset all memory history")