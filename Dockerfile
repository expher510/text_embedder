# Use the official Python 3.11 image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install FastAPI and Uvicorn
RUN pip install fastapi uvicorn

# Copy the current directory contents into the container at /app
COPY . /app

# Expose the port for the application
EXPOSE 8080

# Command to run the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]