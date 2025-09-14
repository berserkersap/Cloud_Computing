# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY fastapi_server.py .

# Expose port 8000 for the Uvicorn server
EXPOSE 8000

# Run the Uvicorn server when the container launches
# --host 0.0.0.0 makes it accessible from outside
# --port 8000 specifies the port
# fastapi_server:app points to the 'app' instance in the 'fastapi_server.py' file # Run with multiple workers (use env var or default 4)
# CMD ["uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["sh", "-c", "uvicorn fastapi_server:app --host 0.0.0.0 --port 8000 --workers ${UVICORN_WORKERS:-4}"]

