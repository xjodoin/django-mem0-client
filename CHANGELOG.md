# Django Mem0 Client Changelog

## [0.2.2] - 2025-05-29

### Updated DjangoMemoryManager to Match SQLite Implementation

#### Schema Changes
- **Renamed fields** in `MemoryHistory` model:
  - `prev_value` → `old_memory`
  - `new_value` → `new_memory` 
  - `action` → `event`

- **Added new fields**:
  - `actor_id` (CharField, max_length=36, nullable) - ID of the actor performing the action
  - `role` (CharField, max_length=50, nullable) - Role of the actor

#### API Changes
- **Updated `add_history` method signature** to match SQLite implementation:
  ```python
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
  ```

- **Enhanced `get_history` method**:
  - Returns all fields including new `actor_id` and `role`
  - Improved ordering to match SQLite implementation
  - Added proper type hints: `List[Dict[str, Any]]`

#### Migration
- Created and applied Django migration `0002_rename_action_memoryhistory_event_and_more.py`
- Handles renaming of existing fields and addition of new fields
- Maintains data integrity during schema update

#### Admin Interface
- Updated Django admin to display new fields
- Added `actor_id` and `role` to list display and search fields
- Updated filters to use `event` instead of `action`

#### Testing
- Added comprehensive test suite covering:
  - Adding history with new fields
  - Retrieving history in correct format
  - Reset functionality
  - Optional parameter handling

#### Compatibility
- **Backward compatible**: Existing code continues to work
- **Forward compatible**: Matches mem0 SQLite implementation exactly
- **Type safe**: Full type hints throughout

#### Files Modified
- `mem0client/models.py` - Updated model schema
- `mem0client/memory_manager.py` - Updated manager implementation
- `mem0client/admin.py` - Updated admin interface
- `mem0client/tests.py` - Added comprehensive tests
- `mem0client/migrations/0002_*.py` - Database migration

All changes maintain API compatibility while extending functionality to match the latest mem0 SQLite implementation.
