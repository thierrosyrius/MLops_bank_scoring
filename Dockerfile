# 1. Use an official Python runtime as a base image
FROM python:3.12-slim

# 2. Set the working directory in the container
WORKDIR /app

# 3. Copy the current directory contents (application files) into the container
COPY . /app

# 4. Install dependencies
# Install necessary system dependencies first
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies (streamlit, lightgbm, etc.)
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose the port Streamlit will run on (default is 8501)
EXPOSE 8070

# 6. Command to run the Streamlit app when the container starts
CMD ["streamlit", "run", "app.py"]
