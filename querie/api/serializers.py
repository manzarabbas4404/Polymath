from querie.models import QueryLog
from rest_framework import serializers


class QueryLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryLog
        fields = "__all__"
        read_only_fields = [
            "id",
            "rewritten_query",
            "response",
            "latency_ms",
            "confidence_score",
            "created_at",
            "updated_at",
        ]
