# Step 1: Use an official lightweight Python runtime environment as base layer
FROM python:3.10-slim

# Step 2: Set secure absolute working directory boundaries inside the container
WORKDIR /app

# Step 3: Prevent Python from writing pyc files to disk and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Step 4: Install system-level dependencies required for compilation tasks
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy dependency manifest layer first to optimize Docker cache layers
COPY requirements.txt /app/

# Step 6: Install locked python dependencies matrix directly inside the sandbox
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the rest of the application source code files into the container space
COPY mainupdate.py model.pkl index.html /app/

# Step 8: Expose network gateway port 8000 outward for internal container routing
EXPOSE 8000

# Step 9: Define the immutable production entry-point executable command
CMD ["uvicorn", "mainupdate:app", "--host", "0.0.0.0", "--port", "8000"]