# slim python base image from Docker Hub
FROM python:3.12-slim

# working directory for the application
WORKDIR /app

# copy local project files into the container --> maybe mount later
COPY . /app

# install python dependencies 
RUN pip install --no-cache-dir -r requirements.txt

# (eventually) expose the port 
EXPOSE 80

# start the application
CMD ["python", "llm_test.py"]
