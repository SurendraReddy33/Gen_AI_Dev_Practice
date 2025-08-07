# Use official Python base image
FROM python:3.11-slim
 
# Set the working directory
WORKDIR /app
 
# Copy all files into the container
COPY requirements.txt .
 
# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 5000
EXPOSE 5000
 
# Run the Flask app
CMD ["python", "app.py"]
 
 