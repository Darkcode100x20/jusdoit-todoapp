# Use Python 3.11
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file first to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Create data directory
RUN mkdir -p /data

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:$PYTHONPATH
ENV FLASK_APP=app.todolist
ENV FLASK_ENV=development

# Run database initialization and migrations
COPY init_db.py .
RUN python init_db.py 2>&1 || (echo "Init DB failed" && python init_db.py 2>&1 && exit 1)

# The CMD is now in docker-compose.yml, but we'll keep a default here just in case
CMD ["python", "todolist.py"]  