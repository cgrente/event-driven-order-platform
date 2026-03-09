FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies first to improve Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source after dependencies.
COPY tracker.py .

CMD ["python", "tracker.py"]