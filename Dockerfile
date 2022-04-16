# Set base image (host OS)
FROM python:3.8-alpine

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev

# By default, listen on port 80
EXPOSE 80

# Set the working directory in the container
WORKDIR /.

# Copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

# Install any dependencies
RUN pip3 install -r requirements.txt

COPY . .

# Specify the command to run on container start
CMD [ "python", "waitress_server.py" ]