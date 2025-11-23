from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Project, Statistic, UserLoginLog


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("MET Details", {"fields": ("role",)}),
    )
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "public_id",
        "idea",
        "user",
        "file_type",
        "file_link",
        "prediction_confidence",
        "verdict",
        "created_at",
    )
    list_filter = ("file_type", "verdict", "created_at")
    search_fields = ("public_id", "idea", "user__username", "file_name")
    readonly_fields = ("file_link", "file_size", "created_at")

    def file_link(self, obj):
        if obj.file:
            return f'<a href="{obj.file.url}" target="_blank">Open File</a>'
        elif obj.link_url:
            return f'<a href="{obj.link_url}" target="_blank">Open Link</a>'
        return "No file"
    file_link.short_description = "File"
    file_link.allow_tags = True


@admin.register(Statistic)
class StatisticAdmin(admin.ModelAdmin):
    list_display = ("metric_name", "metric_value", "project", "recorded_at")
    list_filter = ("metric_name", "recorded_at")
    search_fields = ("metric_name", "project__idea", "notes")


@admin.register(UserLoginLog)
class UserLoginLogAdmin(admin.ModelAdmin):
    list_display = ("user", "login_time", "ip_address")
    list_filter = ("login_time",)
    search_fields = ("user__username", "ip_address")
