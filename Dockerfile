# Dockerfile

FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy the requirements.txt file
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run the application
CMD ["uvicorn", "your_module_name:app", "--host", "0.0.0.0", "--port", "7860"]