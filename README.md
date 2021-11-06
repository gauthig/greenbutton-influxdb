# sce-greenbutton
Parse SCE Green Button download files


## New-Project - ETA of first draft 12/21/2021

Features Planned for v1
- Parse SCE NetMetering version of Green Button CSV file - Solar
- Send data to influxdb (v1, non-ssl) - should be on private network and not public accesible due to no ssl
- Grafana dashbaord to anylze Energy Delivery and Generation
- Manual Download of CSVFile 

## Note - plan is to use CSV file as influxdb ingestion is less cpu intentive when payload is line and not json.  By using CSV file the loading python also has less data to convert to inline format.
