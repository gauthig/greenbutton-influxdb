## Grafana Dashboard Sample
<img src="https://github.com/gauthig/greenbutton-influxdb/blob/main/images/Grafana_dashboard.jpeg" alt="Sample Grafana Dashboard" title="Green Button Grafana Dashboard">


# Green button import to Influxdb
Parse SCE Green Button download files only for now. 
<br>Green button data from utilities is not always the same format so this is tuned to SCE's net metering format.  Yes, Even SCE has several formats based on customer plan.
If someone provides sample data for other green button formats (including SCE non Net Metering) I will incorporate.  

Looking for contributors for other utility formats, code enhancements, bugs, documentation ....
If you would like to contribute anything including just identifying enhancements or bugs, please see the [contributor guide](https://github.com/gauthig/greenbutton-influxdb/blob/main/documentation/contributing.md)

## Still in progress - here is what is completed and works

Features
- [X] Parse SCE NetMetering version of Green Button CSV file - Solar
 File is grouped by day by Received (Sent to Utility) or Delivered (from Utiliy)
- [X] Parse SCE non-Netmetering version of Green Button CSV file - Normal Residential Customers without solar
 File is group by day and has Consumed header tag
- [X] Send data to influxdb (v1, non-ssl) - should be on private network and not public accessible due to no SSL
- [X] Grafana dashboard to analyze Energy Delivery and Generation
- [X] Simple parsed CSV file for use in excel, manual influxdb or other database
- [X] JSON file output format. One closed xml line for each measuremnt
- [ ] SSL support
- [ ] Support for influxdb2
- [X] JSON config file to retain settings for repeat runs
- [X] Convert to PEP 8 style guide

## Requirements
- python3 needs to be installed along with PIP
- make sure required libraries are installed using pip3 or homebrew, see the requirements file or run the command
# pip install -r requirements.txt
 or
# pip3 install -r requirements.txt
<br>

- Must have access to influxdb v1 

- Update energyimport.json parameter file

- Run the program, to test you can use the SCE-NEMFILE.sample file

## Usage
### greenbutton_import.py [-h] [--version] -f FILE [-v] [-q] [-c] [-j] [--createdb] [--nodb]

<br>Loads Green Button csv file and send formated results to influxdb. Used for Net Metering format only
(solar)
<br>
<br>optional arguments:
<br>  -h, --help            show this help message and exit
<br>  --version             display version number
<br>  -f FILE, --file FILE  *REQUIRED* filename of the utility provided csv kwh file
<br>  -v, --verbose         verbose output - send copy of each line to stdout
<br>  -q, --quiet           do not print totals output
<br>  -c, --csv             sends parsed data to a csv delimited file
<br>  -j, --json            sends parsed data to a json file
<br>  --createdb            Drop database and create a new one
<br>  --nodb                Will NOT import to influxdb. Use with -o for local file only

## Output of program 
The following four values are the output:<br>
<br><b>measurement --</b> Either delivered (power from the utility)  or generated (solar power sent to the utility)
<br><b>month --</b> Name value of Month for influxql grouping
<br><b>time --</b> Converted based on the time zone parameter, format is YYYY-MM-DD HH:MM:SS
<br><b>value --</b>  Kilo Watt Hours - decimal precision is based on what the raw utility file is

## References ##
- FAQ's and general information is in the Wiki
- How to [contribute and create issues](https://github.com/gauthig/greenbutton-influxdb/blob/main/documentation/contributing.md)


