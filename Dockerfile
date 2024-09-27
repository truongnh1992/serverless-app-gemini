# Python image to use.
FROM python:3.9-slim-buster

# Install system-level dependencies for grpcio
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev

# Set the working directory to /app
WORKDIR /app

# copy the requirements file used for dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the working directory contents into the container at /app
COPY . .

# Run app.py when the container launches
ENTRYPOINT ["python", "gemini-app.py"]
