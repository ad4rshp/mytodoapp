from django.contrib import admin
from .models import Task # Import your Task model
from django.contrib.auth.models import User # Import User model if needed for display
from django.db.models import F # For more advanced filtering/ordering if needed
from datetime import date

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    # list_display controls which fields are displayed on the change list page of the admin.
    # By including 'user', you'll see which user owns each task.
    # 'description' will show the task description.
    # 'status' and 'due_date' provide quick overview of the task's state.
    list_display = ('user', 'description', 'status', 'due_date', 'complete_date', 'created_at')

    # list_filter creates a sidebar that lets users filter the change list by the fields in list_filter.
    # 'user' and 'status' are great candidates for filtering tasks.
    list_filter = ('user', 'status', 'due_date')

    # search_fields adds a search box to the change list page.
    # You can search tasks by description and by the username of the owner.
    search_fields = ('description__icontains', 'user__username__icontains')

    # raw_id_fields can be useful for ForeignKey fields when you have many related objects.
    # Instead of a dropdown, it provides a text input for the ID, with a lookup button.
    raw_id_fields = ('user',)

    # date_hierarchy adds a date-based drilldown navigation to the change list page.
    # Useful for quickly navigating by date.
    date_hierarchy = 'created_at'

    # readonly_fields makes specified fields non-editable in the admin form.
    # 'created_at' and 'updated_at' are typically auto-generated.
    readonly_fields = ('created_at', 'updated_at')

    # fieldsets controls the layout of edit forms.
    # It allows you to group related fields together.
    fieldsets = (
        (None, {
            'fields': ('description', 'user')
        }),
        ('Task Details', {
            'fields': ('due_date', 'status', 'complete_date'),
            'classes': ('collapse',), # Makes this section collapsible
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )

    # You can also customize actions that appear in the admin's dropdown.
    # For example, an action to mark selected tasks as complete.
    actions = ['mark_tasks_complete', 'mark_tasks_in_progress']

    def mark_tasks_complete(self, request, queryset):
        # Update the status of selected tasks to 'complete' and set complete_date
        updated_count = queryset.update(status='complete', complete_date=date.today())
        self.message_user(request, f"{updated_count} tasks marked as complete.")
    mark_tasks_complete.short_description = "Mark selected tasks as complete"

    def mark_tasks_in_progress(self, request, queryset):
        # Update the status of selected tasks to 'in-progress' and clear complete_date
        updated_count = queryset.update(status='in-progress', complete_date=None)
        self.message_user(request, f"{updated_count} tasks marked as in-progress.")
    mark_tasks_in_progress.short_description = "Mark selected tasks as in progress"

