# Multi-stage build: First stage to build the Kotlin JAR
FROM gradle:7-jdk11 AS builder

# Set the working directory
WORKDIR /app

# Copy the Gradle files
COPY build.gradle.kts settings.gradle.kts ./
COPY build-jar.gradle.kts ./

# Copy the source code
COPY src ./src

# Build the fat JAR
RUN gradle -b build-jar.gradle.kts fatJar --no-daemon

# Debug: List the build directory contents to see what JAR files are created
RUN find build -name "*.jar" -type f || echo "No JAR files found"
RUN ls -la build/ || echo "build directory not found"
RUN ls -la build/libs/ || echo "build/libs directory not found"

# Second stage: Python runtime with the built JAR
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies including OpenJDK 17
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

# Copy the current directory contents into the container at /app
COPY . .

# Build the fat JAR using Gradle
RUN ./gradlew -b build-jar.gradle.kts fatJar

# Debug: List contents of build directory
RUN ls -la build/libs/

# Copy the fat JAR to the libs directory
RUN mkdir -p libs && cp build/libs/*.jar libs/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run api.py when the container launches
CMD ["python", "api.py"]
