FROM python:3.9-slim

# Prevents python from  writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# Python output sent directly to terminal
ENV PYTHONUNBUFFERED 1
# Prevents pip from caching packages, which reduces image size
ENV PIP_NO_CACHE_DIR 1
# No, AI did not write these comments, I wrote them by hand
# I asked it for recommendations to see if I fucked up somewhere

WORKDIR /app

# System dependencies, specifically for ah uhhhhhhh psycopg2 and fucken uhhhhh pandas
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY src/* ./

#ThingyFuckenMagic about not running it as the root user ¯\_(ツ)_/¯
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "Producer.py"]