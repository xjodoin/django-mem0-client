from django.contrib import admin

from .models import MemoryHistory


@admin.register(MemoryHistory)
class MemoryHistoryAdmin(admin.ModelAdmin):
    list_display = ('memory_id', 'event', 'created_at', 'is_deleted', 'actor_id', 'role')
    list_filter = ('event', 'is_deleted', 'role')
    search_fields = ('memory_id', 'old_memory', 'new_memory', 'actor_id')
    date_hierarchy = 'created_at'
