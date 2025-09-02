# Use a stable Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a default port (choose one you want, e.g., 8000)
EXPOSE 8000

# Command to run the application with Gunicorn
CMD gunicorn --workers=4 --bind 0.0.0.0:8000 app:app