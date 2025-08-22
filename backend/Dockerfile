# Stage 1: Build stage - Install dependencies
FROM python:3.12-slim AS builder

WORKDIR /app

# Install uv, the Python package installer
RUN pip install uv

# Copy requirements and install dependencies into a virtual environment
COPY requirements.txt .
RUN uv venv /opt/venv
RUN . /opt/venv/bin/activate && uv pip install --no-cache -r requirements.txt

# Stage 2: Production stage
FROM python:3.12-slim

# Install sqlite3 client
RUN apt-get update && apt-get install -y sqlite3 && rm -rf /var/lib/apt/lists/*

# Create a non-root user
RUN useradd --create-home appuser
WORKDIR /home/appuser/app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Copy application code from the app directory
COPY ./app .

# Change ownership of the app directory and the virtual environment
RUN chown -R appuser:appuser /home/appuser/app && chown -R appuser:appuser /opt/venv

# Switch to the non-root user
USER appuser

# Add venv to the PATH
ENV PATH="/opt/venv/bin:$PATH"

# Make port 8000 available
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
