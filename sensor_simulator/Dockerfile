# Use an official Python runtime as a parent image
FROM python:3.11-slim

WORKDIR /app

COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENV NAME World

CMD ["python", "sensor_script.py"]
