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
import sys, csv, datetime, time

prevarg = ''
influx_url = ''
input_file = ''
csvfileout = ''
dry_run = 'false'
verbose = 'false'
silent_run = 'false'
writer = ''

def help_text():
    print ('\nUsage:\n')
    print ('sceinfluxdb.py -i inputfile -u http://influxdb.mydomain.com')
    print ('          or ')
    print ('python3 sceinfluxdb.py -i inputfile -u http://influxdb.mydomain.com:8086\n')  
    print ('\nBoth input file and URL are requried unless running a dry run\n')      
    print ('Options:')
    print (' -s    Silent - no outputdurring or after valid run')
    print (' -v    Verbose - all parsed data will be sent to standard output')
    print (' -d    Dry Run - parsed records will be sent to a file and not influxdb')
    print ('                 you do nto have to provide -i if -d is used\n')
    return()

def parseData(input_file, writer):
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
                if dry_run == 'true' :
                    writer.writerow([times[1].strip(),row[1], tag])
                if verbose == 'true' :
                    print([times[1].strip(),row[1], tag])

    return(rows_delivered, rows_generated )
          
if __name__ == '__main__':
    for i, arg in enumerate(sys.argv):
        if arg == '-h':
            help_text()
            sys.exit()
        elif arg == '-v':
            print ('csv2log.py - version', __version__)
            sys.exit()
        elif prevarg == "-i" :
            input_file = arg
        elif prevarg == "-u" :
            influx_url = arg
        elif arg == '-v':
            verbose = 'true'
        elif arg == '-s':
            silent_run = 'true'
        elif arg == '-d':
            dry_run = 'true'
        prevarg = arg
    if input_file == '':
        help_text()
        sys.exit('correct parameters not provided')
    if influx_url == '' and dry_run == 'false':
        help_text()
        sys.exit('correct parameters not provided')
    if dry_run == 'true':
        current_date = datetime.datetime.now()
        csvfileout = 'load.' + str(int(current_date.strftime("%Y%m%d%H%M%S"))) + '.csv'
        outfile = open(csvfileout, mode = 'w')
        writer = csv.writer(outfile)
        print("outfile", csvfileout)
    stats_count = parseData(input_file, writer)
    if silent_run == 'false':
        print("Import Complete")
        print("Energy Delivered rows ", stats_count[0])
        print("Energy Generated rows ", stats_count[1])
exit