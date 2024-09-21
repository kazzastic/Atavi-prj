# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies for building Python packages and OpenGL
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libtiff-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the current directory contents into the container at /app
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Change directory to yolov10 and install it
WORKDIR /app/inference/yolov10
RUN pip install -r requirements.txt && pip install -e .

# Return to the original working directory (/app)
WORKDIR /app

# Expose the port that FastAPI will run on
EXPOSE 8080

# Command to run the application
CMD ["uvicorn", "server.src.server:app", "--host", "0.0.0.0"]
