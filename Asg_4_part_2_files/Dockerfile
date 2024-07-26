ARG BASE_IMAGE=python:3.10-slim-buster
FROM $BASE_IMAGE

WORKDIR /app

# Copy all files from the current directory to the container
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install fastapi uvicorn pydantic

# Install any additional dependencies from requirements.txt if it exists
RUN if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python3", "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]