FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (if needed for pandas/numpy)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Expose port (Render will set PORT env var)
EXPOSE 10000

# Run with gunicorn
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:10000"]
