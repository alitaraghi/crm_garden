from django.urls import path

from . import views

app_name = "crm"

urlpatterns = [
    path("clients/", views.ClientListView.as_view(), name="client_list"),
    path("clients/add/", views.ClientCreateView.as_view(), name="client_create"),
]
