# Use an official Python runtime as a parent image
FROM python:3.9-slim-bookworm

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random

# Create a non-root user
RUN groupadd -r tarot && useradd -r -g tarot tarot

# Set the working directory in the container
WORKDIR /app

# Copy requirements first for better cache utilization
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p /app/static/img && \
    chown -R tarot:tarot /app

# Switch to non-root user
USER tarot

# Make port 80 available
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]