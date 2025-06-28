# Use official Python image
FROM python:3.10-slim

# Set timezone environment variable (for IST)
ENV TZ=Asia/Kolkata

# Install tzdata to support timezone changes
RUN apt-get update && apt-get install -y tzdata && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Set working directory
WORKDIR /app

# Copy backend and frontend
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Flask port
EXPOSE 8000

# Run app
CMD ["python", "app.py"]
