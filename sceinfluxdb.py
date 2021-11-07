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
__version__ = "1.0.1"
__VersionDate__ = "9/4/2021"
__maintainer__ = "gauthig@github"
__github__  = "https://github.com/gauthig/scegreenbutton"
__email__ = "garrett-g@outlook.com"
__status__ = "Production"
__status__ = "Production"

from influxdb import InfluxDBClient
from pytz import timezone
import sys, csv, datetime, time, argparse, gzip

prevarg = ''
influx_url = ''
input_file = ''
csvfileout = ''
dry_run = 'false'
verbose = 'false'
silent_run = 'false'
writer = ''


def parseData(input_file, writer, csvout):
    datapoints = []
    rows_generated = 0
    rows_delivered = 0
    row_num = 0
    tag = ''
    infile = open(input_file, mode = 'r')
    csv_reader = csv.reader(infile, delimiter=',')
    for row in csv_reader:
#        row_num = row_num +1
#        print (row_num)
        if len(row) > 0:
            if 'Received' in row[0]:
                tag = 'generated'
#               print('generated')
            elif 'Delivered' in row[0]:
                tag = 'delivered'
#                print('delivered')
            elif 'to' in row[0]:
                times = row[0].split('to')
                if tag == 'generated':
                    rows_generated = rows_generated + 1
                elif tag == 'delivered':
                    rows_delivered = rows_delivered +1
                if csvout :
                    writer.writerow([times[1].strip(),row[1], tag])
                if verbose == 'true' :
                    print([times[1].strip(),row[1], tag])

    return(rows_delivered, rows_generated )
          
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="display version number", action="store_true")
    parser.add_argument("--file", help="filename of the sce greenbutton data")
    parser.add_argument("--host", help="the influxdb host name, no port or http\n example\n --host influxdb.mydomain.com")
    parser.add_argument("--verbose", help="verbose output - send copy of each line to stdout", action="store_true")
    parser.add_argument("--silent", help= "do not print totals output", action="store_true")
    parser.add_argument("--port", help="port of the influxdb, if not provided it will default to 8086")
    parser.add_argument("--csvout", help="sends parsed data to a csvfile instead of sending to influxdb. \n --host and --port are ignored", action="store_true")
    args = parser.parse_args()

    if args.version:
            print ('sceinfluxdb.py - version', __version__)
            sys.exit()


    if args.csvout:
        current_date = datetime.datetime.now()
        csvfileout = 'load.' + str(int(current_date.strftime("%Y%m%d%H%M"))) + '.csv'
        outfile = open(csvfileout, mode = 'w')
        writer = csv.writer(outfile)
        print("outfile", csvfileout)
    
    stats_count = parseData(args.file, writer, args.csvout)
    
    if not args.silent:
        print("Import Complete")
        print("Energy Delivered rows ", stats_count[0])
        print("Energy Generated rows ", stats_count[1])

exit