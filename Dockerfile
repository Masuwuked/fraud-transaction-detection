FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
  python3-dev \
  apt-utils \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

RUN pip install pip==23.0 setuptools==65.5.0

COPY requirements_api.txt .
RUN pip install -r requirements_api.txt \
    && pip install scikit-learn==1.0.2 numpy==1.21.6

RUN pip uninstall -y uvloop

COPY . .

CMD uvicorn app:app --host 0.0.0.0 --port 8000