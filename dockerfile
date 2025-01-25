# Use official Python image from the Docker Hub
FROM python:3.8-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt into the container (if you have one, otherwise we can install directly)
COPY requirements.txt ./

# Install the required Python libraries
RUN pip install --no-cache-dir transformers torch

# Copy the application code into the container
COPY . /app

# Set the entrypoint to run the Python script when the container starts
CMD ["python", "summarizer.py"]
