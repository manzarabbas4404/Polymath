import hashlib
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError

from document.models import Document
from document.api.serializers import DocumentSerializer, DocumentUploadSerializer
from document.services.tasks import process_document


def generate_checksum(file):
    hasher = hashlib.sha256()
    for chunk in file.chunks():
        hasher.update(chunk)
    return hasher.hexdigest()


class DocumentViewSet(
    GenericViewSet,
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
):
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user

        if not user.is_authenticated:
            return Document.objects.none()

        return Document.objects.all().order_by("-created_at")

    def get_serializer_class(self):
        return (
            DocumentUploadSerializer
            if self.action == "create"
            else DocumentSerializer
        )

    def perform_create(self, serializer):
        file = self.request.FILES.get("file")

        if not file:
            raise ValidationError("File is required")

        if file.size > 50 * 1024 * 1024:
            raise ValidationError("File too large (max 50MB)")

        checksum = generate_checksum(file)

        # prevent duplicates (important for AI pipeline later)
        if Document.objects.filter(checksum=checksum).exists():
            raise ValidationError("Duplicate file already exists")

        instance = serializer.save(
            file_size=file.size,
            checksum=checksum
        )

        process_document.delay(instance.id)
