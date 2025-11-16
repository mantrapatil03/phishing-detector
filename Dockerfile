FROM python:3.9-slim

WORKDIR /app

# Install system deps (for selenium if used)
RUN apt-get update && apt-get install -y wget unzip && \
    wget -q https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && mv chromedriver /usr/local/bin/ && rm chromedriver_linux64.zip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY . .

# Expose port
EXPOSE 5000

# Train model on build
RUN python -m src.train

# Run API
CMD ["python", "-m", "src.api"]