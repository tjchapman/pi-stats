FROM python:3.12-slim-bookworm

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files into /app
COPY . . 

EXPOSE 3000

# Command to run the application
CMD ["python","server.py"]