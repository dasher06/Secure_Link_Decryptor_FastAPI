# Use the official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all app files
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port Cloud Run expects
EXPOSE 8080

# Use Gunicorn with Uvicorn worker for FastAPI
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--bind", "0.0.0.0:8080"]
