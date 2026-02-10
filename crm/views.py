from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView

from .models import Client


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
