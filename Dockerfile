# Use a stable Python base image
FROM python:3.10-slim

# Set environment variables to prevent Python from writing pyc files and buffering logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port (Heroku provides PORT dynamically)
EXPOSE $PORT

# Command to run the application with Gunicorn
CMD gunicorn --workers=4 --bind 0.0.0.0:$PORT app:app
