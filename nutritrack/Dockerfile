# Official Python image from Docker Hub
FROM python:3.10

# Working directory
WORKDIR /app

# Requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Nutritrack folder content copy into the container
COPY . .

# Port
EXPOSE 32223

# Run main.py
CMD ["python", "main.py"]
