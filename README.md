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
- [X] JSON config file to retain settings for repeat runs
- [ ] Convert to PEP 8 style guide

## Requirements
- python3 nees to be installed along with PIP
- make sure required libraries are installed using pip3 or homebrew, see the requirements file or run the command
# pip install -r requirements.txt
 or
# pip3 install -r requirements.txt
<br>

- Must have access to influxdb v1 

- Update energyimport.json paramter file

- Run the program, to test you can use the SCE-NEMFILE.sample file

## Usage
### usage: greenbutton_import.py [-h] [--version] -f FILE [-v] [-q]  [-o] [--createdb]

Loads Green Button (Residential Energy Usage) csv file and send formatted results to influxdb.Used for Net Metering format only (solar)

optional arguments:
<br>  -h, --help            show this help message and exit
<br>   --version             display version number
<br>   -f FILE, --file FILE  *REQUIRED* filename of the utility provided csv kwh file
<br>   -v, --verbose         verbose output - send copy of each line to stdout
<br>   -q, --quiet           do not print totals output
<br>   -o, --csvout          sends parsed data to a csvfile. -p can be used or omitted with -o
<br>   --createdb            Drop database and create a new one.

## Output of program 
The following three values are the output:<br>
<br><b>measurement --</b> Either delivered (power from the utility)  or generated (solar power sent to the utility)
<br><b>time --</b> Converted based on the timezone parameter, format is YYYY-MM-DD HH:MM:SS
<br><b>value --</b>  Kilo Watt Hours - decimal percision is based on what the raw utility file is


## Notes ##
- Why did I use csv and not xml?  Sending xml to influx works great but is converted and consumes high memory/cpu.  Many people are running this type of influx/grafana stack on a RasberryPI and thus running with csv, allows for an entire year of import to take a few seconds and little memory. 
- Why unsecure influxdb v1? It is a very common stack used on private networks, but strongly recomned all home users to start using secure engines in thier home network to practice Privacy by Design.   Also as to why InfluxDB v1 at all, InfluxDB v2 changed from sql to thier own language and some basic functions are missing.  I am working on a InfluxDB V2 version and using flux for the grafana dashboard
- Why only Southern California Edison?  Green Button Data is provided by most utlities as a standard US Department of Energy Standard. But the output format is not standardized.  Please create an issue and provide a sample for any other utilites.  This also includes non-Solar sample files.  If you do, make sure you blank out any personal information inthe file like your account number or address.  If you want to add logic to parse another file format, please contact me to be a contributor.  
- How can I get more details of my energy usage?  Look at something like VUE (https://www.emporiaenergy.com/) and then bring that data back with other github projects.
- 
