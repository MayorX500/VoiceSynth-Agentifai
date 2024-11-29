# Use Node.js 18 alpine as the base image
FROM node:18-alpine

# Define default values for the environment variables
ENV API_IPADD=localhost
ENV API_PORT=5000
ENV PORT=3000

# Set timezone to Europe/Lisbon and install tzdata
ENV TZ=Europe/Lisbon

# Install tzdata
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/${TZ} /etc/localtime && \
    echo "${TZ}" > /etc/timezone

# Set working directory
WORKDIR /app

# Copy the entire project directory into the container (adjust to only copy required files)
COPY app .

# Remove node_modules and package-lock.json if they exist (to avoid conflicts)
RUN rm -rf node_modules package-lock.json

# Install npm dependencies
RUN npm install

# Expose the application port
EXPOSE ${PORT}

# Start the application
CMD ["npm", "start"]
