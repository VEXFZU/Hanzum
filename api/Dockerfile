FROM python:3.10.15-slim-bookworm

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY api/requirements.txt /app/api/

RUN pip install -r api/requirements.txt

COPY api /app/api

EXPOSE 8000

HEALTHCHECK CMD curl --fail http://localhost:8000/

ENTRYPOINT ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
