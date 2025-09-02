# Use a stable Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Expose the port your app will run on
ENV PORT=8000
EXPOSE 8000

# Run the app with Gunicorn
CMD ["gunicorn", "--workers=4", "--bind", "0.0.0.0:8000", "app:app"]
