from django.db import models
from document.model_managers import DocumentManager
from core.model_managers import ActiveManager
from core.models import BaseModel
from django.core.exceptions import ValidationError


class DocumentType(models.TextChoices):
    PDF = "PDF", "PDF"
    TXT = "TXT", "Text"
    CSV = "CSV", "CSV"


class Document(BaseModel):
    objects = models.Manager()
    active = DocumentManager()

    organization_id = models.UUIDField(db_index=True)  # future-proof

    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="documents/")
    doc_type = models.CharField(
        max_length=10,
        choices=DocumentType.choices,
        db_index=True
    )

    file_size = models.BigIntegerField(null=True, blank=True)
    checksum = models.CharField(max_length=64, unique=True)  # deduplication

    class Meta:
        indexes = [
            models.Index(fields=["organization_id", "doc_type"]),
            models.Index(fields=["created_at"]),
        ]

    def clean(self):
        if self.file_size and self.file_size > 50 * 1024 * 1024:
            raise ValidationError("File too large (max 50MB)")


class Chunk(BaseModel):
    objects = models.Manager()
    active = ActiveManager()

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="chunks", db_index=True, )

    text = models.TextField()

    chunk_index = models.IntegerField()
    token_count = models.IntegerField(null=True, blank=True)

    # Pinecone reference
    embedding_id = models.CharField(max_length=255, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=["document", "chunk_index"]),
            models.Index(fields=["embedding_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["document", "chunk_index"],
                name="unique_chunk_per_document"
            )
        ]
