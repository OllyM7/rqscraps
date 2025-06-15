# Use official Python image
FROM python:3.11-slim

# Install Node.js and npm
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies (if requirements.txt exists)
RUN if [ -f IGV2/requirements.txt ]; then pip install --no-cache-dir -r IGV2/requirements.txt; fi

# Install Node.js dependencies (if package.json exists)
RUN if [ -f package.json ]; then npm install; fi

# Default command (can be overridden in Coolify)
CMD ["python", "IGV2/scrape_instagram_reels.py", "nasa", "--format", "both"] 