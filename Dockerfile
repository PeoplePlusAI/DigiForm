# Pull base image
FROM ubuntu:22.04

ENV TZ=Asia/Kolkata
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-opencv \
    ffmpeg \
    tesseract-ocr

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install python dependencies
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Copy project
COPY . .
