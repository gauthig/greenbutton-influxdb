# sce-greenbutton
Parse SCE Green Button download files
Green button data from utilities is not always the same format so this is tuned to SCE's net metering format.  Yes, Even SCE has several formats based on cusomer plan.
If someone provides sample data for other green button formats (including SCE non Net Metering) I will incorporate.  

Looking for contributors that want to change the parsing function to parse their format of data.  Will add a command line option to set which format to parse to. 

## Still in progress - here is what is completed and works

Features
- [X] Parse SCE NetMetering version of Green Button CSV file - Solar
- [ ] Parse SCE non-Netmetering version of Green Button CSV file - Normal Residential Customers without solar
- [X] Send data to influxdb (v1, non-ssl) - should be on private network and not public accessible due to no SSL
- [ ] Grafana dashboard to analyze Energy Delivery and Generation
- [X] Create formatted text file for use in other programs (Formatted for Influxdb)
- [X] Create simple parsed CSV file for use in excel or other database
- [ ] SSL support
- [ ] Support for influxdb2
- [ ] Add yaml options file to retain settings for repeat runs
- [ ] Convert to PEP 8 style guide

## Program Setup 
- python3
- make sure the following libraries are install using pip3 or homebrew, see the requirements file
  - influxdb
  - json
  - argparse
- Run the program

## Usage
### usage: sceinfluxdb.py [-h] [--version] -f FILE [-n HOSTNAME] [-v] [-q] [-P PORT] [-o] [-b BATCHSIZE]
###                      [--dbname [DBNAME]] [-u [USER]] [-p [PASSWORD]] [-tz TIMEZONE] [--createdb]

Loads SCE Green Button csv file and send formatted results to influxdb.Used for Net Metering format only (solar)

optional arguments:
<br>  -h, --help            show this help message and exit
<br>   --version             display version number
<br>   -f FILE, --file FILE  filename of the sce greenbutton data
<br>   -n HOSTNAME, --hostname HOSTNAME
                        the influxdb host name, no port or http example --host influxdb.mydomain.com
<br>   -v, --verbose         verbose output - send copy of each line to stdout
<br>   -q, --quiet           do not print totals output
<br>   -P PORT, --port PORT  port of the influxdb, if not provided it will default to 8086
<br>   -o, --csvout          sends parsed data to a csvfile. -p can be used or omitted with -o
<br>   -b BATCHSIZE, --batchsize BATCHSIZE
                        Batch size. Default: 5000.
<br>   --dbname [DBNAME]     Database name. Required if -n and -p used
<br>   -u [USER], --user [USER]
                        influxdb userid
<br>   -p [PASSWORD], --password [PASSWORD]
                        Influxdb password
<br>   -tz TIMEZONE, --timezone TIMEZONE
                        Timezone of supplied data. Default: UTC
<br>   --createdb            Drop database and create a new one.



## Notes ##
- Why did I use csv and not xml?  Sending xml to influx works great but is converted and consumes high memeory/cpu.  Many people are running this type of influx/grafana stack on a RasberryPI and thus running with csv, allows for an entire year of import to take a few seconds and little memory. 
- Why unsecure influxdb v1? It is a very common stack used on private networks, but strongly recomned all home users to start using secure engines in thier home network to practice Privacy by Design.   Also as to why InfluxDB v1 at all, InfluxDB v2 changed from sql to thier own language and some basic functions are missing.
- How can I get more details of my energy usage?  Look at something like VUE (https://www.emporiaenergy.com/) and then bring that data back with other github projects.
- 
