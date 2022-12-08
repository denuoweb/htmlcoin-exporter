# syntax=docker/dockerfile:1

# Use the Python v3.10.8 alpine image
FROM python:3.10.8-alpine

# Add container image title and description
LABEL org.opencontainers.image.title="htmlcoin-exporter"
LABEL org.opencontainers.image.description="A Prometheus exporter for Htmlcoin nodes."

# Set the working directory to /htmlcoin-exporter
WORKDIR /htmlcoin-exporter

# Copy the current directory contents into the container at /htmlcoin-exporter
COPY . /htmlcoin-exporter

# Upgrade PIP package to latest
RUN python -m pip install --upgrade pip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port number
EXPOSE 6363

# Set endpoint for Htmlcoin-Exporter monitor and run the project
ENTRYPOINT ["python", "monitor.py"]
