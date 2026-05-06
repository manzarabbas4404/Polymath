from django.contrib import admin
from document.models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "doc_type", "file_size", "created_at")


admin.site.register(Document, DocumentAdmin)