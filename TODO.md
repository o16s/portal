- automate single sensor creation using API. minimal api request below.

- architecture:


ParentDevice (has lastSample JSONObject attribute, uses attributeLinks to write to SensorA.attr1 and SensorB.attr1)
- SensorA (attr1, attr2)
- SensorB (attr1)
- SensorC (attr1)


To automate:
1. create parent device with POST. note down parentId.

2. create all Sensors and their attributes with POST:
{
  "name": "NewMy",
  "parentId": "4qLQQHBhRNW8cwMU5RCn43",
  "realm": "demo-makatcandy",
  "type": "ThingAsset",

   "attributes": {
   "notes": {},
   "location": {},
}

Add all returned IDs to a list.


3. update parent device with attributelinks to all sensors:


{
  "name": "NewMy",
  "parentId": "4qLQQHBhRNW8cwMU5RCn43",
  "realm": "demo-makatcandy",
  "type": "ThingAsset",

   "attributes": {
   "notes": {},
   "location": {},
   "lastSample": {
     "name": "lastSample",
     "type": "JSONObject",
     "meta": {
        "accessRestrictedRead": true,
        "accessRestrictedWrite": true,
        "storeDataPoints": true,
        "attributeLinks" : [
            {"ref": {"id": "7NRFpebtbzf4VLfqwckN2B", "name": "attr1"}, "filters": [{"type": "jsonPath", "path": "$.sensor_name_short.attr1", "returnFirst": true, "returnLast": false}]}
            {"ref": {"id": "7NRFpebtbzf4VLfqwckN2B", "name": "attr2"}, "filters": [{"type": "jsonPath", "path": "$.sensor_name_short.attr2", "returnFirst": true, "returnLast": false}]}
        ]
     }
   }
}
}



4. on device MQTT client, publish to parent device topic with lastSample attribute:

{
    "sensor_name_short" : {
        "attr1": 1,
        "attr2": 2
    },
    "sensor_name_short2" : {
        "attr1": 1
    }
    "sensor_name_short3" : {
        "attr1": 1
    }
}


POST all attributes, then PUT the lastSample attribute with the attributeLinks

POST https://portal.octanis.ch/api/master/asset
{
  "name": "NewMy",
  "parentId": "4qLQQHBhRNW8cwMU5RCn43",
  "realm": "demo-makatcandy",
  "type": "ThingAsset",

   "attributes": {
   "notes": {},
   "location": {},
   "lastSample": {
     "name": "lastSample",
     "type": "JSONObject",
     "meta": {
        "accessRestrictedRead": true,
        "accessRestrictedWrite": true,
        "storeDataPoints": true,
        "attributeLinks" : [
            {"ref": {"id": "7NRFpebtbzf4VLfqwckN2B", "name": "magnitude_mean"}, "filters": [{"type": "jsonPath", "path": "$.magnitude_mean", "returnFirst": true, "returnLast": false}]}
        ]
     }
   }
}
}

