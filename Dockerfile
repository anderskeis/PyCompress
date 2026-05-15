FROM python:3.12-slim

WORKDIR /app

# Install build dependencies for Pillow-SIMD (compiles from source with SIMD)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libjpeg62-turbo-dev \
        zlib1g-dev \
        libwebp-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

ENTRYPOINT ["python", "main.py"]
