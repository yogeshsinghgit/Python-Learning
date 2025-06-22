FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy and install dependencies first (cache-friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY ./app /app

# Run the app using uvicorn when container starts
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
