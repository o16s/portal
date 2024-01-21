#!/bin/bash

set -e

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | sed 's/#.*//g' | xargs)
else 
    echo ".env file not found."
    exit 1
fi

# Check if OR_HOSTNAME is set
if [ -z "$OR_HOSTNAME" ]; then
    echo "OR_HOSTNAME not set in .env file."
    exit 1
fi

# check $PROJECT_NAME is set
if [ -z "$PROJECT_NAME" ]; then
    echo "PROJECT_NAME not set in .env file."
    exit 1
fi

# Ask for the secret
read -sp 'Enter the secret: ' secret
echo

# Clean and install the distribution
./gradlew clean installDist

# Get deployment and manager version from git
DEPLOYMENT_VERSION=$(git rev-parse --short HEAD)
MANAGER_VERSION=$(cd openremote; git rev-parse --short HEAD; cd ..)

# Build docker images
docker build -t openremote/manager:$MANAGER_VERSION ./openremote/manager/build/install/manager/
docker build -t openremote/portal-deployment:$DEPLOYMENT_VERSION ./deployment/build/


# Shutdown existing services
DEPLOYMENT_VERSION=$(git rev-parse --short HEAD) OR_ADMIN_PASSWORD=$secret OR_HOSTNAME=$OR_HOSTNAME docker-compose -p $PROJECT_NAME down

# Remove the existing data volume
docker volume rm portal_deployment-data

# Start services with the new configuration
DEPLOYMENT_VERSION=$(git rev-parse --short HEAD) OR_ADMIN_PASSWORD=$secret OR_HOSTNAME=$OR_HOSTNAME docker-compose -p $PROJECT_NAME up -d
