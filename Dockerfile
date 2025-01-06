# lightweight Python base image
FROM python:3.10-slim

# working directory in the container
WORKDIR /app

# Copying the requirements file and install dependencies
COPY app/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copying the entire project directory into the container
COPY . .

# Specifying the default command to run the application
CMD ["python", "run.py"]
