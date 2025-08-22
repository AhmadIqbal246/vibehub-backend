FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better for caching)
COPY backend/requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose port
EXPOSE 8000

# Run Daphne server
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
