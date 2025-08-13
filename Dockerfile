FROM python:3.12-slim

# Install CA certificates and update them
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && update-ca-certificates

# Set environment variables to disable SSL verification for development
ENV PYTHONHTTPSVERIFY=0
ENV PYTHONIOENCODING=utf-8
ENV CURL_CA_BUNDLE=""
ENV REQUESTS_CA_BUNDLE=""
ENV PYTHONUNBUFFERED=1

# Upgrade pip and install certifi to latest
RUN pip install --no-cache-dir --upgrade pip certifi

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . .

# Run the Python bot
CMD ["python", "main.py"]
