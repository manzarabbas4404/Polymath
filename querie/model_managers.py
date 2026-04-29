from django.db import models
from core.model_managers import ActiveManager


class QueryManager(ActiveManager):
    def recent(self):
        return self.get_queryset().order_by("-created_at")
