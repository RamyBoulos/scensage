# Use official lightweight Python image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source code into container
COPY . .

# Set environment variable to make sure imports work
ENV PYTHONPATH=/app

# Default command to run (shows help)
CMD ["python", "scenesage/scenesage.py", "--help"]