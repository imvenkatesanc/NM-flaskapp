FROM python:3.9

WORKDIR /app

# Copy the application files to the container
COPY ./Demo /app

# Set the working directory to /app/Demo
WORKDIR /app/Demo

# Install application dependencies
RUN pip install -r requirements.txt

# Expose the desired port
EXPOSE 5000

# Set the command to run the application
CMD ["python", "app.py"]
