import logging
from typing import Any, Dict, List, Optional

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

    def add_history(
        self,
        memory_id: str,
        old_memory: Optional[str],
        new_memory: Optional[str],
        event: str,
        *,
        created_at: Optional[str] = None,
        updated_at: Optional[str] = None,
        is_deleted: int = 0,
        actor_id: Optional[str] = None,
        role: Optional[str] = None,
    ) -> None:
        """
        Add a history entry for a memory.

        Args:
            memory_id (str): ID of the memory.
            old_memory (str): Previous value of the memory.
            new_memory (str): New value of the memory.
            event (str): Event performed on the memory (ADD, UPDATE, DELETE).
            created_at (str, optional): Creation timestamp. Defaults to None.
            updated_at (str, optional): Update timestamp. Defaults to None.
            is_deleted (int, optional): Whether the memory is deleted. Defaults to 0.
            actor_id (str, optional): ID of the actor performing the action. Defaults to None.
            role (str, optional): Role of the actor. Defaults to None.
        """
        # Create the history entry in the Django model
        MemoryHistory.objects.create(
            memory_id=memory_id,
            old_memory=old_memory,
            new_memory=new_memory,
            event=event,
            created_at=created_at,
            updated_at=updated_at,
            is_deleted=bool(is_deleted),
            actor_id=actor_id,
            role=role
        )

        logger.info(f"Added history for memory {memory_id} with event {event}")

    def get_history(self, memory_id: str) -> List[Dict[str, Any]]:
        """
        Get the history for a memory.

        Args:
            memory_id (str): ID of the memory.

        Returns:
            List[Dict[str, Any]]: List of history entries for the memory.
        """
        history_entries = MemoryHistory.objects.filter(
            memory_id=memory_id
        ).order_by('created_at', 'updated_at')

        # Convert Django model instances to dictionaries
        result = []
        for entry in history_entries:
            history_dict = {
                "id": str(entry.id),
                "memory_id": entry.memory_id,
                "old_memory": entry.old_memory,
                "new_memory": entry.new_memory,
                "event": entry.event,
                "created_at": entry.created_at,
                "updated_at": entry.updated_at,
                "is_deleted": entry.is_deleted,
                "actor_id": entry.actor_id,
                "role": entry.role,
            }

            result.append(history_dict)

        return result

    def reset(self):
        """
        Reset the history store.
        """
        MemoryHistory.objects.all().delete()
        logger.warning("Reset all memory history")
