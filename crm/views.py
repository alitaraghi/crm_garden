from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .models import Client, Project, Task
from django.db.models import Count
from datetime import date


class ClientListView(LoginRequiredMixin, ListView):
    """List all clients belonging to the current user."""

    model = Client
    template_name = "crm/client_list.html"
    context_object_name = "clients"

    def get_queryset(self):
        return (
            Client.objects.filter(owner=self.request.user)
            .select_related("owner")
            .order_by("name")
        )


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Create a new client owned by the current user."""

    model = Client
    template_name = "crm/client_form.html"
    fields = ["name", "email", "phone", "company", "status", "notes"]
    success_url = reverse_lazy("crm:client_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class OwnerQuerysetMixin(LoginRequiredMixin):
    """Mixin to ensure we only work with objects owned by the current user."""

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class DashboardView(LoginRequiredMixin, ListView):
    """Simple dashboard showing high-level stats for the current user."""

    model = Task
    template_name = "crm/dashboard.html"
    context_object_name = "overdue_tasks"

    def get_queryset(self):
        today = date.today()
        return (
            Task.objects.filter(
                owner=self.request.user,
                due_date__lte=today,
            )
            .exclude(status=Task.STATUS_DONE)
            .select_related("project", "project__client")
            .order_by("due_date")
        )

    def get_context_data(self, **kwargs):
        from .models import Client, Project  # local import to avoid circular issues if any

        context = super().get_context_data(**kwargs)

        user = self.request.user

        # Client count
        client_count = Client.objects.filter(owner=user).count()

        # Project counts by status
        project_counts = (
            Project.objects.filter(owner=user)
            .values("status")
            .annotate(total=Count("id"))
        )

        # Task counts by status
        task_counts = (
            Task.objects.filter(owner=user)
            .values("status")
            .annotate(total=Count("id"))
        )

        context["client_count"] = client_count
        context["project_counts"] = project_counts
        context["task_counts"] = task_counts
        context["today"] = date.today()

        return context

class ClientDetailView(OwnerQuerysetMixin, DetailView):
    """Show details for a single client."""

    model = Client
    template_name = "crm/client_detail.html"
    context_object_name = "client"


class ClientUpdateView(OwnerQuerysetMixin, UpdateView):
    """Update an existing client."""

    model = Client
    template_name = "crm/client_form.html"
    fields = ["name", "email", "phone", "company", "status", "notes"]

    def get_success_url(self):
        return reverse_lazy("crm:client_detail", kwargs={"pk": self.object.pk})


class ClientDeleteView(OwnerQuerysetMixin, DeleteView):
    """Delete an existing client."""

    model = Client
    template_name = "crm/client_confirm_delete.html"
    success_url = reverse_lazy("crm:client_list")

class ProjectListView(OwnerQuerysetMixin, ListView):
    """List all projects belonging to the current user."""

    model = Project
    template_name = "crm/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("client", "owner").order_by("-created_at")


class ProjectCreateView(LoginRequiredMixin, CreateView):
    """Create a new project for a given client."""

    model = Project
    template_name = "crm/project_form.html"
    fields = ["name", "description", "status", "start_date", "due_date"]

    def dispatch(self, request, *args, **kwargs):
        self.client = get_object_or_404(
            Client,
            pk=self.kwargs["client_pk"],
            owner=request.user,
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.client = self.client
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = self.client
        return context

    def get_success_url(self):
        return reverse_lazy("crm:client_detail", kwargs={"pk": self.client.pk})
    
class ProjectDetailView(OwnerQuerysetMixin, DetailView):
    """Show details for a single project."""

    model = Project
    template_name = "crm/project_detail.html"
    context_object_name = "project"


class ProjectUpdateView(OwnerQuerysetMixin, UpdateView):
    """Update an existing project."""

    model = Project
    template_name = "crm/project_form.html"
    context_object_name = "project"
    fields = ["name", "description", "status", "start_date", "due_date"]

    def get_success_url(self):
        return reverse_lazy("crm:project_detail", kwargs={"pk": self.object.pk})


class ProjectDeleteView(OwnerQuerysetMixin, DeleteView):
    """Delete an existing project."""

    model = Project
    template_name = "crm/project_confirm_delete.html"
    success_url = reverse_lazy("crm:project_list")

class TaskListView(OwnerQuerysetMixin, ListView):
    """List all tasks belonging to the current user."""

    model = Task
    template_name = "crm/task_list.html"
    context_object_name = "tasks"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.select_related("project", "project__client", "owner", "assigned_to").order_by(
            "status",
            "-priority",
            "due_date",
        )

class TaskCreateView(LoginRequiredMixin, CreateView):
    """Create a new task for a given project."""

    model = Task
    template_name = "crm/task_form.html"
    fields = ["title", "description", "assigned_to", "status", "priority", "due_date"]

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(
            Project,
            pk=self.kwargs["project_pk"],
            owner=request.user,
        )
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.instance.project = self.project
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project"] = self.project
        return context

    def get_success_url(self):
        return reverse_lazy("crm:project_detail", kwargs={"pk": self.project.pk})

class TaskDetailView(OwnerQuerysetMixin, DetailView):
    """Show details for a single task."""

    model = Task
    template_name = "crm/task_detail.html"
    context_object_name = "task"


class TaskUpdateView(OwnerQuerysetMixin, UpdateView):
    """Update an existing task."""

    model = Task
    template_name = "crm/task_form.html"
    context_object_name = "task"
    fields = ["title", "description", "assigned_to", "status", "priority", "due_date"]

    def get_success_url(self):
        return reverse_lazy("crm:task_detail", kwargs={"pk": self.object.pk})


class TaskDeleteView(OwnerQuerysetMixin, DeleteView):
    """Delete an existing task."""

    model = Task
    template_name = "crm/task_confirm_delete.html"
    success_url = reverse_lazy("crm:task_list")
