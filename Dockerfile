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

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Upgrade pip and install certifi to latest (suppress root warning)
RUN pip install --no-cache-dir --upgrade --root-user-action=ignore pip certifi

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

# Copy all project files and set ownership
COPY . .
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Run the Python bot
CMD ["python", "main.py"]
