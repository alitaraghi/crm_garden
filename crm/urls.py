from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    # Client URLs
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/add/", views.ClientCreateView.as_view(), name="client_create"),
    path("clients/<int:pk>/", views.ClientDetailView.as_view(), name="client_detail"),
    path("clients/<int:pk>/edit/", views.ClientUpdateView.as_view(), name="client_update"),
    path("clients/<int:pk>/delete/", views.ClientDeleteView.as_view(), name="client_delete"),

    # Project URLs
    path("projects/", views.ProjectListView.as_view(), name="project_list"),
    path(
        "clients/<int:client_pk>/projects/add/",
        views.ProjectCreateView.as_view(),
        name="project_create_for_client",
    ),
]
