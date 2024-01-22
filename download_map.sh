#!/bin/bash

# Check if exactly three arguments are provided
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 MAX_ZOOM MIN_ZOOM REGION"
    exit 1
fi

# Assign arguments to variables
MAX_ZOOM=$1
MIN_ZOOM=$2
REGION=$3

# Save the current directory
CURRENT_DIR=$(pwd)

# Exit script if any command fails
set -e

# Change directory to the parent directory
cd ..

# Clone the repository
git clone https://github.com/openmaptiles/openmaptiles.git

# Navigate to the cloned directory
cd openmaptiles

# Edit the .env file
sed -i "s/MAX_ZOOM=.*/MAX_ZOOM=$MAX_ZOOM/" .env
sed -i "s/MIN_ZOOM=.*/MIN_ZOOM=$MIN_ZOOM/" .env

# Source the env file
source .env

# Run the quickstart script with the region parameter
./quickstart.sh $REGION

# Ask user for confirmation before overwriting
echo "Are you sure you want to overwrite the existing mbtiles file? [y/N]"
read -r confirmation
if [[ $confirmation =~ ^[Yy]$ ]]
then
    # Copy the generated .mbtiles file back to the original directory
    cp data/$REGION.mbtiles "$CURRENT_DIR/deployment.local/mapdata/mapdata.mbtiles"
    echo "File copied successfully."
else
    echo "Operation aborted by the user."
fi

# Print message to user
echo "Don't forget to edit mapsettings.json and restart openremote."

# Return to the original directory
cd "$CURRENT_DIR"