# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for psycopg2, Pillow, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY backend/requirements.txt /app/
# Copy project files
COPY . .
# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files
COPY . /app/

# Expose the port Railway will use
EXPOSE 8000

# Default command to run your app (ASGI with Daphne)
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
