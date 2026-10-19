FROM python:3.10-slim

# Install system dependencies required to build dlib/face_recognition and run OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    cmake \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgtk-3-dev \
    libboost-all-dev \
    libopenblas-dev \
    liblapack-dev \
    libjpeg-dev \
    zlib1g-dev \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 5000

# Use gunicorn for production; run with 4 workers
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
