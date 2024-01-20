Place the map tiles in this directory. The tiles should be in the MBTiles format. The file should be named `mapdata.mbtiles`.

on lasso:
wget https://download.geofabrik.de/europe-latest.osm.pbf

git clone https://github.com/systemed/tilemaker.git
cd tilemaker
docker build -t tilemaker .

docker run --rm -it -v $(pwd):/srv tilemaker --input=/srv/europe-latest.osm.pbf --output=/srv/mapdata.mbtiles
