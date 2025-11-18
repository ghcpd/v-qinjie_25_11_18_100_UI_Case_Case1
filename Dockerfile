# Dockerfile for running the web application
FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY buggy/package.json ./buggy/
COPY fixed/package.json ./fixed/

# Install dependencies
RUN cd buggy && npm install && \
    cd ../fixed && npm install

# Copy application files
COPY buggy/ ./buggy/
COPY fixed/ ./fixed/

# Expose port
EXPOSE 8080

# Default to running buggy version
WORKDIR /app/buggy
CMD ["npx", "http-server", "-p", "8080", "--cors"]

