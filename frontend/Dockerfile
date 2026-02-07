# Frontend Streamlit - Serverless (Cloud Run)
FROM python:3.11-slim

WORKDIR /app

RUN groupadd --gid 1000 app && useradd --uid 1000 --gid app --shell /bin/bash app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chown -R app:app /app
USER app

EXPOSE 8080

ENV PORT=8080
# Streamlit mặc định 8501; Cloud Run dùng 8080
CMD ["streamlit", "run", "app.py", "--server.port=8080", "--server.address=0.0.0.0"]

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=2 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080')" || exit 1
