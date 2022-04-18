# Set base image (host OS)
FROM python:3.8-alpine

# By default, listen on port 80
EXPOSE 80

COPY . .

# Install any dependencies
RUN pip3 install -r requirements.txt

# Specify the command to run on container start
CMD [ "python", "waitress_server.py" ]