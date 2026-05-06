import hashlib
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader
from pinecone import Pinecone
import os


# 1. Extract text
def extract_text(file_path):
    reader = PdfReader(file_path)
    text = ""

    for page in reader.pages:
        text += page.extract_text() or ""

    return text


# 2. Chunk text
def chunk_text(text):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )
    return splitter.split_text(text)


# Pinecone client (lazy init)
def get_pc():
    return Pinecone(api_key=os.environ["PINECONE_API_KEY"])


def get_index():
    pc = get_pc()
    return pc.Index("polymath-index")


# 3. Embed + upload
def embed_and_store(chunks, document_id):

    pc = get_pc()
    index = get_index()

    vectors = []

    for i, chunk in enumerate(chunks):

        res = pc.inference.embed(
            model="llama-text-embed-v2",
            inputs=[chunk],
            parameters={"input_type": "passage"}
        )

        vectors.append({
            "id": f"{document_id}_{i}",
            "values": res.data[0].values,
            "metadata": {
                "text": chunk,
                "document_id": str(document_id),
                "chunk_index": i
            }
        })

    # 🔥 THIS WAS MISSING
    index.upsert(vectors=vectors)