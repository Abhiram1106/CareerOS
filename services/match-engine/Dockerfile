FROM python:3.11-slim

WORKDIR /app

# libgomp1 is required by PyTorch CPU builds
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
# CPU-only torch from the dedicated whl index (avoids pulling full CUDA image)
RUN pip install --no-cache-dir \
    torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

# Pre-cache MiniLM weights at build time — no HuggingFace hit at container start.
ENV HF_HOME=/app/.cache/huggingface
RUN python -c "\
from sentence_transformers import SentenceTransformer; \
SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2', \
cache_folder='/app/.cache/huggingface')" \
    && echo 'MiniLM cached.'

COPY app ./app

# ChromaDB persists to /app/chroma_data — mount a volume in compose for durability
ENV CHROMA_DATA_DIR=/app/chroma_data
RUN mkdir -p /app/chroma_data

EXPOSE 8005
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8005"]
