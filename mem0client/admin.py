from django.contrib import admin

from .models import MemoryHistory


@admin.register(MemoryHistory)
class MemoryHistoryAdmin(admin.ModelAdmin):
    list_display = ('memory_id', 'action', 'created_at', 'is_deleted')
    list_filter = ('action', 'is_deleted')
    search_fields = ('memory_id', 'prev_value', 'new_value')
    date_hierarchy = 'created_at'
