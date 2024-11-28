### WIP ###

FROM ubuntu:20.04

# Define default values for the Enviroment Variables
ENV SERVER_IPADD localhost
ENV SERVER_PORT 5000
ENV PORT 3000

# Set timezone to Europe/Lisbon (Portugal) and install tzdata
ENV DEBIAN_FRONTEND=noninteractive 
ENV TZ=Europe/Lisbon

# Install tzdata
RUN apt-get update && apt-get install -y tzdata

# Update apt
RUN apt-get update && \
    apt-get install -y software-properties-common

# Install app packages
RUN apt-get update && apt-get install -y \
   nodejs \
   npm

# Clone app directory
WORKDIR /app

# Copy the entire project directory into the container (adjust to only copy required files)
COPY app .

# Install App npm
RUN npm install

# I don't think EXPOSE really does much of practical interest.
# If you docker run -P then Docker will publish all exposed ports on to random host ports,
# but that's of minimal usefulness; you're better off explicitly docker run -p to explicitly
# publish individual ports, which don't necessarily need to be "exposed".
#
# The only thing that really leaves is, like labels, information that can be found
# by docker inspect on an image. I don't know if there are any tools that display than information.
# But I'd probably leave the EXPOSE line in my Dockerfile as a hint to the next person to maintain 
# the system as to what I expect it to do.
EXPOSE ${PORT}

# Start TTS_App
CMD npm start