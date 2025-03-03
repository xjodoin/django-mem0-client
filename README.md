# Django Mem0 Client

[![PyPI version](https://badge.fury.io/py/django-mem0-client.svg)](https://badge.fury.io/py/django-mem0-client)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Django implementation of the [mem0](https://github.com/mem0ai/mem0) memory system, using Django models for storing memory history instead of SQLite directly.

## Overview

This project provides a Django-based client for the mem0 memory system. It maintains full compatibility with the original mem0 implementation while leveraging Django's ORM capabilities for memory history storage.

Key benefits:
- Integration with Django's powerful ORM
- Admin interface for viewing and managing memory history
- Seamless integration with existing Django applications
- Maintains all vector store and embedding functionality from mem0

## Installation

### Installation from PyPI

The easiest way to install is from PyPI:

```bash
pip install django-mem0-client
```

### Prerequisites

- Python 3.8+
- Django 4.0+
- mem0 library

### Setting Up in Your Django Project

1. Add 'mem0client' to your INSTALLED_APPS in settings.py:
```python
INSTALLED_APPS = [
    # ...
    'mem0client',  # Not 'django-mem0-client'
    # ...
]
```

2. Apply migrations to set up the database:
```bash
python manage.py migrate
```

3. Create a superuser for the admin interface (optional):
```bash
python manage.py createsuperuser
```

## Usage

### Basic Usage

```python
import os
import django
from mem0.configs.base import MemoryConfig

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
django.setup()

# Import after Django setup
from mem0client.memory_client import DjangoMemory

# Create a memory client with default configuration
memory = DjangoMemory()

# Add a memory
result = memory.add(
    messages="John likes to play tennis on Tuesdays with his friend Mike.",
    user_id="user123",
    agent_id="agent456"
)

# Search for memories
search_results = memory.search(query="tennis", user_id="user123")

# Get memory history
memory_id = search_results["results"][0]["id"]
history = memory.history(memory_id)
```

### Using Configuration Options

You can customize the memory client using the same configuration options as the original mem0 library:

```python
from mem0.configs.base import MemoryConfig
from mem0client.memory_client import DjangoMemory

# Create a configuration with custom settings
config = MemoryConfig(
    embedding_model="text-embedding-3-small",  # OpenAI embedding model to use
    vector_store_path="./vector_store",        # Path to store vectors
    distance_metric="cosine",                  # Distance metric for vector search
    add_timestamps=True,                       # Add timestamps to memories
    chunk_size=1000,                           # Size of text chunks
    chunk_overlap=200,                         # Overlap between chunks
)

# Create a memory client with custom configuration
memory = DjangoMemory(config)
```

### Using from_config Method

You can also initialize the client using a dictionary of configuration options:

```python
from mem0client.memory_client import DjangoMemory

# Configuration as a dictionary
config_dict = {
    "embedding_model": "text-embedding-3-small",
    "vector_store_path": "./vector_store",
    "distance_metric": "cosine",
    "add_timestamps": True,
    "chunk_size": 1000,
    "chunk_overlap": 200,
}

# Create a memory client from config dictionary
memory = DjangoMemory.from_config(config_dict)
```

Refer to the [official mem0 documentation](https://github.com/mem0ai/mem0) for a complete list of configuration options and their meanings.

### Running the Example Script

```bash
python example_usage.py
```

### Using the Admin Interface

1. Start the Django development server:
```bash
python manage.py runserver
```

2. Open your browser and go to `http://127.0.0.1:8000/admin/`

3. Log in with your superuser credentials

4. Navigate to the "Memory histories" section to view and manage memory history entries

## API Reference

The `DjangoMemory` class implements the `MemoryBase` interface from mem0 and provides the following methods:

- `add(messages, user_id=None, agent_id=None, run_id=None, metadata=None, filters=None, prompt=None)`: Create a new memory
- `get(memory_id)`: Retrieve a memory by ID
- `get_all(user_id=None, agent_id=None, run_id=None, limit=100)`: List all memories
- `search(query, user_id=None, agent_id=None, run_id=None, limit=100, filters=None)`: Search for memories
- `update(memory_id, data)`: Update a memory by ID
- `delete(memory_id)`: Delete a memory by ID
- `delete_all(user_id=None, agent_id=None, run_id=None)`: Delete all memories matching filters
- `history(memory_id)`: Get the history of changes for a memory
- `reset()`: Reset the memory store

Detailed API documentation can be found in the [mem0 official documentation](https://github.com/mem0ai/mem0#api-reference).

## Configuration

The client accepts the same configuration parameters as the original mem0 `Memory` class through the `MemoryConfig` object. See the [mem0 configuration documentation](https://github.com/mem0ai/mem0#configuration) for details.

## Integration with Existing Django Projects

To integrate with an existing Django project:

1. Add 'mem0client' to your `INSTALLED_APPS` in settings.py:
```python
INSTALLED_APPS = [
    # ...
    'mem0client',
    # ...
]
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Import and use the `DjangoMemory` class in your views or services:
```python
from mem0client.memory_client import DjangoMemory

# Create a memory client
memory = DjangoMemory()

# Use memory client methods...
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Here's how you can contribute:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

### Development

For local development:

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install in development mode: `pip install -e .`
5. Run tests: `python manage.py test mem0client`

## Publishing to PyPI

For maintainers who want to publish new versions to PyPI:

1. Update the version number in `setup.py` and `__init__.py`
2. Create a new distribution:
   ```bash
   python setup.py sdist bdist_wheel
   ```
3. Upload to PyPI:
   ```bash
   python -m twine upload dist/*
   ```

Note: You'll need `twine` installed (`pip install twine`) and PyPI credentials configured.