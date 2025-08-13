FROM python:3.12-slim

# Install system dependencies including Chromium (alternative to Chrome)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    curl \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver \
    # Chrome/Chromium dependencies
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libwayland-client0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxkbcommon0 \
    libxrandr2 \
    xdg-utils \
    && rm -rf /var/lib/apt/lists/*

# Verify Chromium installation
RUN chromium --version

# Set environment variables to disable SSL verification for development
ENV PYTHONHTTPSVERIFY=0
ENV PYTHONIOENCODING=utf-8
ENV CURL_CA_BUNDLE=""
ENV REQUESTS_CA_BUNDLE=""
ENV PYTHONUNBUFFERED=1

# Create a non-root user with proper permissions
RUN groupadd -r appuser && useradd -r -g appuser -m appuser

# Create cache directories with proper permissions
RUN mkdir -p /home/appuser/.cache/selenium \
    && chown -R appuser:appuser /home/appuser/.cache

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

# Set Chrome/Chromium path for webdriver-manager
ENV PATH="/usr/bin:${PATH}"
ENV DISPLAY=:99
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Run the Python bot
CMD ["python", "main.py"]
