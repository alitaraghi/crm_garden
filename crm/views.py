from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404
from .models import Client, Project


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
