from celery import shared_task
from django.conf import settings
from document.models import Document
from document.services.ingestion import extract_text, chunk_text, embed_and_store


@shared_task
def process_document(document_id):
    doc = Document.objects.get(id=document_id)

    file_path = doc.file.path

    # 1. extract
    text = extract_text(file_path)

    # 2. chunk
    chunks = chunk_text(text)

    # 3. embed + store
    embed_and_store(chunks, doc.id)