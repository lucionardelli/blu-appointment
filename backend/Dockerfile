FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install sqlite3 command-line tool
RUN apt update && apt install -y \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install uv, the Python package installer
RUN pip install uv

# Copy and install the requirements
COPY ./requirements.txt /app/requirements.txt
RUN uv pip install --system --no-cache -r /app/requirements.txt

# Copy the rest of the backend application's source code from the host to the container
COPY . /app

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define environment variable
ENV APP_MODULE="app.main:app"

# Run uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
