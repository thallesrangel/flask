FROM python:3.11-slim-buster

# Set working directory
WORKDIR /app

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the port on which the Flask app will listen
EXPOSE 5000

# Define the command to run the Flask app
CMD ["python", "app.py"]