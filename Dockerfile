FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements_api.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_api.txt
RUN pip uninstall -y uvloop

# Copy app code
COPY . .

# Run API
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]