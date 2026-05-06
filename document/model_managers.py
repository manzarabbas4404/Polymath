from django.db import models
from core.model_managers import ActiveManager


class DocumentManager(ActiveManager):
    def by_type(self, doc_type):
        return self.get_queryset().filter(doc_type=doc_type)
