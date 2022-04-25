# Set base image (host OS)
# FROM python:3.8-alpine
FROM amancevice/pandas:1.4.2-alpine

RUN apk update && apk add gcc libc-dev make git libffi-dev openssl-dev python3-dev libxml2-dev libxslt-dev 

# By default, listen on port 80
EXPOSE 80

COPY . .

RUN pip3 install --upgrade pip

# Install any dependencies
RUN pip3 install -r requirements.txt

# Specify the command to run on container start
CMD [ "python", "waitress_server.py" ]
