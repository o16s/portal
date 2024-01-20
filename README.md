# Custom Project
This repo is a template for custom projects; showing the recommended project structure and including `README` files in the `deployment` directory to provide details about how to customise each part.

## Setup Tasks
The following `OR_SETUP_TYPE` value(s) are supported:

* `production` - Requires `CUSTOM_USER_PASSWORD` environment variable to be specified 

Any other value will result in default setup.

## Encrypted files
If any encrypted files are added to the project then you will need to specify the `GFE_PASSWORD` environment variable to be able to build the project and decrypt the
files.


## Follow these steps to run your custom project

1. cd portal
2. git submodule init; git submodule update --rebase --remote
3. docker-compose -f profile/dev-ui.yml up --build -d 
4. cd openremote/
5. yarn install
6. cd ui/app/manager
7. npm run serve -- --env config=../../../../deployment/manager/app
8. access http://localhost:9000/manager/
Note the UI will access port 8080 which runs the manager api, started by the docker container in step 3.


## Login portal theme is under 

keycloak/themes/octanis

to make new themes, copy the octanis folder and rename it to your theme name, then change the theme name in keycloak/themes/theme.properties

applicationName can be set in login/messages/messages_en.properties



### maptiles

on lasso:
wget https://download.geofabrik.de/europe-latest.osm.pbf

git clone https://github.com/systemed/tilemaker.git
cd tilemaker
docker build -t tilemaker .

docker run --rm -it -v $(pwd):/srv tilemaker --input=/srv/europe-latest.osm.pbf --output=/srv/europe-latest.mbtiles
