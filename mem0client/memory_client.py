from mem0.memory.main import Memory
from mem0.configs.base import MemoryConfig
from typing import Dict, Any

from .memory_manager import DjangoMemoryManager


class DjangoMemory(Memory):
    """
    Django implementation of Memory class that overrides only the necessary methods
    to use Django models for storing memory history instead of SQLite.

    This class inherits from Memory so we can reuse all the existing functionality
    and only override the parts that interact with SQLite.
    """

    def __init__(self, config: MemoryConfig = MemoryConfig()):
        """
        Initialize Django Memory client.

        This overrides the parent class initialization to use DjangoMemoryManager
        instead of SQLiteManager.

        Args:
            config (MemoryConfig): Configuration for the memory client.
        """
        # Call the parent constructor to set up all the standard components
        super().__init__(config)

        # Replace the SQLiteManager with our Django-based manager
        self.db = DjangoMemoryManager()

    @classmethod
    def from_config(cls, config_dict: Dict[str, Any]):
        """
        Create a memory instance from a configuration dictionary.

        This method is kept for API compatibility.

        Args:
            config_dict (Dict[str, Any]): Configuration dictionary.

        Returns:
            DjangoMemory: Instance of the Django memory client.
        """
        return super().from_config(config_dict)