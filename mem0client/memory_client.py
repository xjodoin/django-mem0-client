import logging
from typing import Dict, Any

from mem0.configs.base import MemoryConfig
from mem0.memory.main import Memory
from mem0.utils.factory import EmbedderFactory, VectorStoreFactory, LlmFactory
from pydantic import ValidationError

from .memory_manager import DjangoMemoryManager

logger = logging.getLogger(__name__)


class DjangoMemory(Memory):
    """
    Django implementation of Memory class that overrides only the necessary methods
    to use Django models for storing memory history instead of SQLite.

    This class inherits from Memory so we can reuse all the existing functionality
    and only override the parts that interact with SQLite.
    """

    # noinspection PyMissingConstructor
    def __init__(self, config: MemoryConfig = MemoryConfig()):
        """
        Initialize Django Memory client.

        This overrides the parent class initialization to use DjangoMemoryManager
        instead of SQLiteManager.

        Args:
            config (MemoryConfig): Configuration for the memory client.
        """
        self.config = config

        self.custom_prompt = self.config.custom_prompt
        self.embedding_model = EmbedderFactory.create(self.config.embedder.provider, self.config.embedder.config)
        self.vector_store = VectorStoreFactory.create(
            self.config.vector_store.provider, self.config.vector_store.config
        )
        self.llm = LlmFactory.create(self.config.llm.provider, self.config.llm.config)
        self.db = DjangoMemoryManager()
        self.collection_name = self.config.vector_store.config.collection_name
        self.api_version = self.config.version

        self.enable_graph = False

        if self.config.graph_store.config:
            from mem0.memory.graph_memory import MemoryGraph

            self.graph = MemoryGraph(self.config)
            self.enable_graph = True

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
        try:
            config = MemoryConfig(**config_dict)
        except ValidationError as e:
            logger.error(f"Configuration validation error: {e}")
            raise
        return cls(config)
