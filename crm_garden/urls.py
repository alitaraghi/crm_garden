from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from crm.views import simple_logout

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path(
        "accounts/login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path("accounts/logout/", simple_logout, name="logout"),

    # App
    path("", include("crm.urls", namespace="crm")),
]
