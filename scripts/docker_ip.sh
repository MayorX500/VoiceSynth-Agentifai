#!/bin/ash

# Resolve the IP address of 'api' service
API_IP=$(getent hosts api_container | awk '{ print $1 }')

# Alternatively, you can use 'nslookup' or 'ping' to get the IP
# API_IP=$(nslookup api | awk '/Address: / { print $2 }')
# API_IP=$(ping -c 1 api | head -1 | awk -F'[()]' '{ print $2 }')

# Check if the IP was found
if [ -z "$API_IP" ]; then
	echo "Failed to resolve IP address for 'api'."
	exit 1
fi

echo "Resolved API IP: $API_IP"

# Export the IP address as an environment variable
export REACT_APP_API_IP_ADDRESS=$API_IP

# Start your application
npm start
