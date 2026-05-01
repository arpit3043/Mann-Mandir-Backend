FROM python:3.12-slim

WORKDIR /app

RUN useradd --create-home --shell /bin/bash appuser

COPY mann-mandir-god-service/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY mann-mandir-god-service/ .

ENV PYTHONPATH=/app

RUN chown -R appuser:appuser /app
USER appuser

ENV PORT=8080
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD python -c "import os,urllib.request; urllib.request.urlopen('http://127.0.0.1:%s/health_status'%os.environ.get('PORT',8080))" || exit 1

CMD ["sh", "-c", "exec uvicorn main:app --host 0.0.0.0 --port ${PORT:-8080}"]
