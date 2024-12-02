# Use the official Python image from Docker Hub
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire nutritrack folder content into the container
COPY . .

# Set the environment variable


# Expose a port (change if needed, e.g., 5000 for Flask)
EXPOSE 32223

# Run main.py as the entry point
CMD ["python", "main.py"]
