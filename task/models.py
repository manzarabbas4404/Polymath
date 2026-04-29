from django.db import models
from document.models import BaseModel
from core.model_managers import ActiveManager


class Task(BaseModel):
    objects = models.Manager()
    active = ActiveManager()

    organization_id = models.UUIDField(db_index=True)

    title = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(max_length=50, db_index=True)

    priority = models.CharField(max_length=50, db_index=True)

    created_by = models.UUIDField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["organization_id", "status"]),
            models.Index(fields=["priority"]),
        ]
