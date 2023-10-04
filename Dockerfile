# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory in the container
WORKDIR /PulsePoint

# Copy the requirements file into the container at /app
COPY requirements.txt /PulsePoint/

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /PulsePoint/

# Expose port 8000
EXPOSE 8000

# Run the command to start your Django application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
