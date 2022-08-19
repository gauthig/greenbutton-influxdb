#!/usr/bin/python3 
# -*- coding: utf-8 -*-

#### NOTE ####
# Please make sure your python binary is listed in the first line. 
# i.e. if your python is just python and not python 3 change it. 
# If your python is in /bin or /opt change it
# I know the above statement is normal shell programming, but I have recevied several questions on 'What does bad interpreter mean' 
#

# greenbutton_import.py
# Input - SCE Green Data (TOU Style)
# Output - Inluxdb mesurements  (V1)
#

__author__ = 'Garrett Gauthier'
__copyright__ = 'Copyright 2022, Garrett Gauthier'
__author__ = 'Garrett Gauthier'
__copyright__ = 'Copyright 2022, Garrett Gauthier'
__credits__ = ['Garrett Gauthier', 'Others soon?']
__license__ = 'GPL'
__version__ = '1.1'
__VersionDate__ = '08/18/2022'
__maintainer__ = 'gauthig@github'
__github__ = 'https://github.com/gauthig/scegreenbutton'
__email__ = 'garrett-g@outlook.com'
__status__ = 'Production'
__status__ = 'Production'

from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBClientError
from datetime import datetime
import sys
import csv
import time
import argparse
import json
import pytz


prevarg = ''
influx_url = ''
input_file = ''
csvfileout = ''
dry_run = 'false'
verbose = 'false'
silent_run = 'false'
writer = ''
metricsout = []

def getConfigValue(key, defaultValue):
    if key in config:
        return config[key]
    return defaultValue

def parseData(input_file, orgtimezone,  verbose):
    if verbose:
        print('Starting parseData')

    point = []
    rows_generated = 0
    rows_delivered = 0
    row_num = 0
    tag = ''
    pmult = 0
    dt_format = '%Y-%m-%d %H:%M:%S'
    xtime= ""
    infile = open(input_file, mode='r')
    csv_reader = csv.reader(infile, delimiter=',')
    if verbose:
        print('File: ', infile)
        
    for row in csv_reader:
        if len(row) > 0:
            if 'Received' in row[0]:
                tag = 'generated'
            elif 'Delivered' in row[0]:
                tag = 'delivered'
            elif 'Consumption' in row[0]:
                tag = 'delivered'
            elif 'to' in row[0]:
                sce_timestamp = row[0].split('to')
                # SCE adds non-ASCII charter before the to field, need to strip
                sce_timestamp=[item.replace('\xa0', '') for item in sce_timestamp]
                dt_local = datetime.strptime(sce_timestamp[0], dt_format)
                dt_utc = dt_local.astimezone(pytz.UTC)
                dt_utc = dt_utc.strftime("%Y-%m-%d %H:%M:%S")
                if tag == 'generated':
                    rows_generated = rows_generated + 1
                    pmult = -1
                elif tag == 'delivered':
                    rows_delivered = rows_delivered + 1
                    pmult = 1

            

                point = {
                    "measurement" : "SCE",
                    "tags": {"type": tag},
                    "time": dt_utc,
                    "fields": {"value": float(row[1]) * pmult}
                    }

                metricsout.append(point)

                if verbose:
                    print (point)
 

    return (rows_delivered, rows_generated)


def writedata():
    textout = ''
    current_date = datetime.now()
    fileout = 'energy' + str(int(current_date.strftime('%Y%m%d%H%M'
                               ))) + '.csv'

    #Influxformat
    with open(fileout, 'w', encoding='UTF-8') as f:
        csv_columns = 'measurement,time,value'
        
        #writer = csv.writer(f)
        f.write(csv_columns)
  
        for data in metricsout:
            textout = '\n' +  json.dumps(data)
            textout = textout.replace('{"measurement": "SCE", "tags": {"type": "', '')
            textout = textout.replace('"}, "time": "', ',')
            textout = textout.replace('", "fields": {"value":', ',')
            textout = textout.replace('}}', '')
            f.write(textout)
            print(textout)
            
            
            
    return ()


def senddata(
    hostname,
    port,
    user,
    password,
    dbname,
    batchsize,
    timezone,
    createdb,
    ):

    client = InfluxDBClient(hostname, port, user, password, dbname)

    if createdb == True:
        print ('Deleting database %s' % dbname)
        client.drop_database(dbname)
        print ('Creating database %s' % dbname)
        client.create_database(dbname)

    if len(metricsout) > 0:

        # print('Inserting %d metricsout...'%(len(metricsout)))

        client.switch_user(user, password)

        response = client.write_points(metricsout,batch_size=10000)
            #print("Wrote %d, response: %s" % (len(t), response))

    return ()


if __name__ == '__main__':

    configFilename = 'energyimport.json'
    config = {}
    with open(configFilename) as configFile:
        config = json.load(configFile)
    
    print('Influx Host:', config['host'])
    print('Influx Port:', config['port'])


    parser = \
        argparse.ArgumentParser(description='Loads Green Button csv file and send formated results to influxdb.Used for Net Metering format only (solar)'
                                )
    parser.add_argument('--version', help='display version number',
                        action='store_true')
    parser.add_argument('-f', '--file', required=True,
                        help='*REQUIRED* filename of the utility provided csv kwh file')
    parser.add_argument('-v', '--verbose',
                        help='verbose output - send copy of each line to stdout'
                        , action='store_true')
    parser.add_argument('-q', '--quiet',
                        help='do not print totals output',
                        action='store_true')
    parser.add_argument('-o', '--csvout',
                        help='sends parsed data to a csvfile.  -p can be used or omitted with -o'
                        , action='store_true')
    parser.add_argument('--createdb', action='store_true',
                        default=False,
                        help='Drop database and create a new one.')
    parser.add_argument( '--nodb',
                        help='Will not uplocad to influxdb.  Use with -o or --csvout for local file only'  )                     
    args = parser.parse_args()

    if args.version:
        print ('sceinfluxdb.py - version', __version__)
        sys.exit()


    if args.verbose:
        print ('Parsed arguments')

    (rows_delivered, rows_generated) = parseData(args.file,
            config['timezone'],  args.verbose)

    if args.csvout:
        writedata()

    if not args.nodb:
        senddata(
            config['host'],
            config['port'],
            config['user'],
            config['password'],
            config['dbname'],
            config['batchsize'],
            config['timezone'],
            args.createdb
        )

    if not args.quiet:
        print ('Import Complete')
        print ('Energy Delivered rows ', rows_delivered)
        print ('Energy Generated rows ', rows_generated)

exit