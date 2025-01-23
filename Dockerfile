FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY moderation.py .

# Expose the port the app runs on
EXPOSE 5656

# Command to run the application
CMD ["uvicorn", "moderation.py:app", "--host", "0.0.0.0", "--port", "5656"]