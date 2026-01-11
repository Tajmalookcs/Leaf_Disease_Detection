# Use official Python 3.10 image
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Flask
EXPOSE 5000

# Command to run the app
CMD ["gunicorn", "app = Flask(__name__)", "--bind", "0.0.0.0:5000"]

