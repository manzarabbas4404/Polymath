from rest_framework import serializers
from document.models import Document, Chunk


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"
        read_only_fields = ["id", "checksum",
                            "file_size", "created_at", "updated_at"]


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ["name", "file", "doc_type"]


class ChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chunk
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
