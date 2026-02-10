from django.contrib import admin

from .models import Client, Project, Task


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "company", "status", "owner", "created_at")
    list_filter = ("status", "owner", "created_at")
    search_fields = ("name", "email", "company")
    ordering = ("name",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "status", "owner", "start_date", "due_date")
    list_filter = ("status", "owner", "start_date", "due_date")
    search_fields = ("name", "client__name")
    autocomplete_fields = ("client",)
    ordering = ("-created_at",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "project",
        "status",
        "priority",
        "owner",
        "assigned_to",
        "due_date",
    )
    list_filter = ("status", "priority", "owner", "assigned_to", "due_date")
    search_fields = ("title", "project__name")
    autocomplete_fields = ("project", "assigned_to")
    ordering = ("status", "priority", "due_date")
