from django.urls import path
from django.views.generic import RedirectView

from .views import (
    dashboard_view,
    login_view,
    logout_view,
    profile_view,
    project_view,
    register_view,
    reports_view,
    statistics_view,
    upload_delete_view,
    logo_view,
    poster_view,
    advertisement_view,
    welcome_view,
)

urlpatterns = [
    path("", welcome_view, name="welcome"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path("project/", project_view, name="project"),
    path("statistics/", statistics_view, name="statistics"),
    path("reports/", reports_view, name="reports"),
    path("uploads/<int:pk>/delete/", upload_delete_view, name="upload_delete"),
    path("profile/", profile_view, name="profile"),
    path("logo/", logo_view, name="logo"),
    path("poster/", poster_view, name="poster"),
    path("advertisement/", advertisement_view, name="advertisement"),
    path("register/", register_view, name="register"),
    path("Signup/", RedirectView.as_view(pattern_name="register", permanent=True)),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
]

