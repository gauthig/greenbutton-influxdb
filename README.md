# sce-greenbutton
Parse SCE Green Button download files
Unfortunatly all green button data from utlities does not coem out in the same formay so this is tuned to SCE's net metering format.
If someone provides sample data for other green button formats (including SCE non Net Metering) I will incorporate.  Also would accept controbutors that want to change the parsing function to parse thier format of data.  Will add a command line option to set which format to parse to. 

## New-Project - ETA of first draft 12/01/2021

Features Planned for v1
- Parse SCE NetMetering version of Green Button CSV file - Solar
- Send data to influxdb (v1, non-ssl) - should be on private network and not public accesible due to no ssl
- Grafana dashbaord to anylze Energy Delivery and Generation
- Manual Download of CSVFile 


