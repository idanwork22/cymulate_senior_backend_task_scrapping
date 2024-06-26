# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the application port
EXPOSE 8000

# Define environment variable
ENV MONGO_URI=mongodb://mongodb:27017/

# Run the command to start the FastAPI server
CMD ["uvicorn", "scraper:app", "--host", "0.0.0.0", "--port", "8000"]
