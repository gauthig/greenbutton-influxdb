# Influxdb v1.8 non-ssl (to use influxql instead of FLUX)
# Grafana Latest version

Multi-container Docker app built from the following services:

* [InfluxDB](https://github.com/influxdata/influxdb) - time series database
* [Grafana](https://github.com/grafana/grafana) - visualization UI for InfluxDB



## Requirements

- Install [docker-compose](https://docs.docker.com/compose/install/) on the docker host.
- Clone this repo on the docker host
- Change default credentials or Grafana provisioning and the .env file

## Start up

# First Time 
```
docker-compose up
```
- Watch to make sure no errors
- Bring up a browser and go to http://yourhost:3000
- Sign in with the creditionals in the docker-compose.yml and .env files
- Shut down docker by ctrl-c in the terminal it is running.

# Ongoing
```
docker-compose up -d
```
<br>For your test environment this is fine and docker will not restart each time you reboot.
<br>To make it influxdb/grafana perstiant on a server, uncomment the two (2) lines in <b>docker-compose.yml<b>
- #restart: always

To stop the Influxdb/grafana

```
docker-compose down
```

## Ports

The services in the app run on the following ports:

| Host Port | Service |
| - | - |
| 3000 | Grafana |
| 8086 | InfluxDB |


## Volumes

The app creates the following named volumes (one for each service) so data is not lost when the app is stopped:

* influxdb-storage
* chronograf-storage
* grafana-storage


## Database

<br>The app creates a default InfluxDB database called `energy` for use with the default greenbutton.json
<br>Use the --createdb option when running greenbutton_import.py to create a new db if you changed the databse name in the json file

## Grafana Setup
<br>No Dashboards or datasources are installed with the default grafana
- Create influxdb datasource, connection string would be http://influxdb:8086
- Do not put you domain our server name in as it's within the docker network and must match the docker name.
- Enter the user credtials you setup in docker-compose.yml
- setupt the database name and energy or if you created a new oone use that name
- Dasboard, import json from this github repo called dashboard.json
