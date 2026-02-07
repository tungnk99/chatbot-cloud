# Tools Service - Serverless (Cloud Run)
# Base image Python 3.11
FROM python:3.11-slim

WORKDIR /app

# Non-root user
RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --shell /bin/bash app

# Dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R app:app /app
USER app

EXPOSE 8080

ENV PORT=8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=2 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/health')" || exit 1
