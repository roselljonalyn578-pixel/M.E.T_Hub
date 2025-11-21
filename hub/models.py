from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user that keeps track of whether an account should see the admin
    experience or the standard contributor experience. We rely on Django's
    built-in `is_staff` flag for permission checks but store a friendly label
    for UI use.
    """

    ROLE_CHOICES = [
        ("admin", "Administrator"),
        ("user", "User"),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")

    def is_admin(self) -> bool:
        return self.is_staff or self.role == "admin"


class Project(models.Model):
    FILE_TYPES = [
        ("image", "Image"),
        ("video", "Video"),
        ("link", "Link"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="projects"
    )
    idea = models.CharField(
        max_length=255,
        help_text="A short identifier so you can map predictions back to investigations.",
    )
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(
        upload_to="uploads/",
        blank=True,
        null=True,
        help_text="Required for image/video uploads.",
    )
    link_url = models.URLField(blank=True, help_text="Required for link submissions.")
    description = models.TextField(blank=True)
    file_name = models.CharField(max_length=255, blank=True)
    file_size = models.PositiveIntegerField(default=0)
    public_id = models.CharField(
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        editable=False,
    )
    prediction_confidence = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        default=0,
    )
    verdict = models.CharField(max_length=50, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        db_table = "hub_upload"

    def __str__(self) -> str:
        return f"{self.idea} ({self.file_type})"

    def save(self, *args, **kwargs):
        if not self.idea:
            if self.link_url:
                self.idea = self.link_url
            elif self.file:
                self.idea = Path(self.file.name).name
            else:
                self.idea = "Untitled evidence"

        if self.file_type in {"image", "video"}:
            self.description = ""

        if self.file:
            self.file_name = self.file.name
            self.file_size = self.file.size
        elif self.link_url:
            self.file_name = self.link_url
            self.file_size = 0
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if (is_new or not self.public_id) and self.pk:
            public_id = f"ID{self.pk}"
            Project.objects.filter(pk=self.pk).update(public_id=public_id)
            self.public_id = public_id


class Statistic(models.Model):
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name="statistics"
    )
    metric_name = models.CharField(max_length=100)
    metric_value = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["-recorded_at"]

    def __str__(self) -> str:
        return f"{self.metric_name}: {self.metric_value} ({self.project.idea})"
