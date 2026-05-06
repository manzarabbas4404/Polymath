from django.db import models
from document.models import BaseModel
from querie.model_managers import QueryManager


class QueryLog(BaseModel):
    objects = models.Manager()
    active = QueryManager()

    # organization_id = models.UUIDField(db_index=True)

    user_id = models.UUIDField(null=True, blank=True, db_index=True)

    query_text = models.TextField()

    rewritten_query = models.TextField(null=True, blank=True)

    response = models.TextField(null=True, blank=True)

    latency_ms = models.IntegerField(null=True, blank=True)
    confidence_score = models.FloatField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["user_id"]),
        ]
