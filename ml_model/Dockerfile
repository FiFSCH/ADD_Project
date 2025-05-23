FROM python:3.9-slim

# Based on Czupyt's work
ENV PYTHONDONTWRITEBYTECODE 1
# Python output sent directly to terminal
ENV PYTHONUNBUFFERED 1
# Prevents pip from caching packages, which reduces image size
ENV PIP_NO_CACHE_DIR 1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/* ./

RUN mkdir -p /ml_model
COPY logistic_regression_add.pkl /ml_model/logistic_regression_add.pkl

RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser


CMD ["python", "Model.py"]