# app/Dockerfile

# pull the official docker image
FROM python:3.9.5-slim

# set work directory
WORKDIR vermillion

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY vermillion .

# install dependencies
RUN pip install -r requirements.txt
