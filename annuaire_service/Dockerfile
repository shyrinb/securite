# Dockerfile for auth_service
FROM python:3.9

# Set the working directory to /annuaire_service
WORKDIR /annuaire_service

# Copy the current directory contents into the container at /annuaire_service
COPY . /annuaire_service

RUN pip install -r requirements.txt

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Define environment variable
ENV NAME annuaire_service

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]