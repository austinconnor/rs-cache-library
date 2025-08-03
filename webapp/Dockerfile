# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements-webapp.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements-webapp.txt

# Copy the webapp code
COPY . .

# Make port 5001 available to the world outside this container
EXPOSE 5001

# Run the webapp
CMD ["python", "app.py"]
