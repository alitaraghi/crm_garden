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
    path("projects/<int:pk>/", views.ProjectDetailView.as_view(), name="project_detail"),
    path("projects/<int:pk>/edit/", views.ProjectUpdateView.as_view(), name="project_update"),
    path("projects/<int:pk>/delete/", views.ProjectDeleteView.as_view(), name="project_delete"),
   
    # Task URLs
    path("tasks/", views.TaskListView.as_view(), name="task_list"),
    path(
        "projects/<int:project_pk>/tasks/add/",
        views.TaskCreateView.as_view(),
        name="task_create_for_project",
    ),
    path("tasks/<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
    path("tasks/<int:pk>/edit/", views.TaskUpdateView.as_view(), name="task_update"),
    path("tasks/<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
    # Dashboard URL
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),

]
