# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory to /auth_service
WORKDIR /custom_auth_service

# Copy the current directory contents into the container at /auth_service
COPY . /custom_auth_service

RUN pip install -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8002

# Define environment variable
ENV NAME custom_auth_service

CMD ["python", "manage.py", "runserver", "0.0.0.0:8002"]