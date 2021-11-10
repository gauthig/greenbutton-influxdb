#!/usr/bin/python3
# sceinfluxdb.py
# Input - SCE Green Data (TOU Style)
# Output - Inluxdb mesurements  (V1)
# 

__author__ = "Garrett Gauthier"
__copyright__ = "Copyright 2021, Garrett Gauthier"
__author__ = "Garrett Gauthier"
__copyright__ = "Copyright 2021, Garrett Gauthier"
__credits__ = ["Garrett Gauthier", "Others soon?"]
__license__ = "GPL"
__version__ = "0.5.1"
__VersionDate__ = "11/10/2021"
__maintainer__ = "gauthig@github"
__github__  = "https://github.com/gauthig/scegreenbutton"
__email__ = "garrett-g@outlook.com"
__status__ = "Production"
__status__ = "Production"

from influxdb import InfluxDBClient
#from influxdb.exceptions import InfluxDBClientError
from pytz import timezone
import sys, csv, datetime, time, argparse, gzip, json

prevarg = ''
influx_url = ''
input_file = ''
csvfileout = ''
dry_run = 'false'
verbose = 'false'
silent_run = 'false'
writer = ''
metricsout = []


def parseData(input_file,orgtimezone,verbose):
    point = []
    rows_generated = 0
    rows_delivered = 0
    row_num = 0
    tag = ''
    pmult = 0
    infile = open(input_file, mode = 'r')
    csv_reader = csv.reader(infile, delimiter=',')
    for row in csv_reader:
        if len(row) > 0:
            if "Received" in row[0]:
                tag = 'generated'
            elif 'Delivered' in row[0]:
                tag = "delivered"
            elif 'to' in row[0]:
                times = row[0].split('to')
                if tag == 'generated':
                    rows_generated = rows_generated + 1
                    pmult = -1
                elif tag == 'delivered':
                    rows_delivered = rows_delivered + 1
                    pmult = 1
                #point = {"measurement" : "SCE", "tags": tag, "time": times[1].strip(), "field": row[1] }
                point = [
                    {
                    "measurement": "SCE",
                    "tags": {
                    "type": tag
                    },
                    "time": times[1].strip(),
                    "fields": {
                    "value": float(row[1])*pmult
                    }
                    }
                    ]
                metricsout.append(point)
                if verbose :
                    print(point)
                

    return(rows_delivered,rows_generated)

def writedata():
    current_date = datetime.datetime.now()
    fileout = 'load.' + str(int(current_date.strftime("%Y%m%d%H%M"))) + '.out'
    f = open(fileout, mode = 'w')
    for t in metricsout:
        f.write(json.dumps(t) + '\n')

    
    return()

def senddata(hostname, port,  user, password, dbname, 
        batchsize, timezone, createdb):
    client = InfluxDBClient(hostname, port, user, password, dbname)

    if(createdb == True):
        print('Deleting database %s'%dbname)
        client.drop_database(dbname)
        print('Creating database %s'%dbname)
        client.create_database(dbname)

    if len(metricsout) > 0:
        #print('Inserting %d metricsout...'%(len(metricsout)))
        client.switch_user(user, password)
        for t in metricsout:
            response = client.write_points(t)
        #  print("Wrote %d, response: %s" % (len(t), response))
            
        

    return()
          
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Loads SCE Green Button csv file and send formated results to influxdb.Used for Net Metering format only (solar)")
    parser.add_argument("--version", help="display version number", action="store_true")
    parser.add_argument("-f", "--file", required=True, help="filename of the sce greenbutton data")
    parser.add_argument("-n", "--hostname", help="the influxdb host name, no port or http\n example\n --host influxdb.mydomain.com")
    parser.add_argument("-v", "--verbose", help="verbose output - send copy of each line to stdout", action="store_true")
    parser.add_argument("-q", "--quiet", help= "do not print totals output", action="store_true")
    parser.add_argument("-P", "--port", help="port of the influxdb, if not provided it will default to 8086")
    parser.add_argument("-o", "--csvout", help="sends parsed data to a csvfile.  -p can be used or omitted with -o", action="store_true")
    parser.add_argument('-b', '--batchsize', type=int, default=5000, help='Batch size. Default: 5000.')
    parser.add_argument('--dbname', nargs='?', help='Database name.  Required if -n and -p used')
    parser.add_argument('-u', '--user', nargs='?', help='influxdb userid')
    parser.add_argument('-p', '--password', nargs='?', help='Influxdb password')
    parser.add_argument('-tz', '--timezone', default='UTC', help='Timezone of supplied data. Default: UTC')   
    parser.add_argument('--createdb', action='store_true', default=False, help='Drop database and create a new one.')    
    args = parser.parse_args()

    if args.version:
            print ('sceinfluxdb.py - version', __version__)
            sys.exit()

    rows_delivered, rows_generated = parseData(args.file, args.timezone,args.verbose)
    
    if args.csvout:
        writedata()
        
    
    if args.hostname:
        senddata(args.hostname, args.port,  args.user, args.password, args.dbname, 
        args.batchsize, args.timezone, args.createdb)

    if not args.quiet:
        print("Import Complete")
        print("Energy Delivered rows ", rows_delivered)
        print("Energy Generated rows ", rows_generated)

exit