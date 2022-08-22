#!/usr/bin/python3
# -*- coding: utf-8 -*-

#### NOTE ####
# Please make sure your python binary is listed in the first line.
# i.e. if your python is just python and not python 3 change it.
# If your python is in /bin or /opt change it
# I know the above statement is normal shell programming,
# but I have recevied several questions on 'What does bad interpreter mean'
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
__versiondate__ = '08/18/2022'
__maintainer__ = 'gauthig@github'
__github__ = 'https://github.com/gauthig/scegreenbutton'
__email__ = 'garrett-g@outlook.com'
__status__ = 'Production'
__status__ = 'Production'

from influxdb import InfluxDBClient
#from influxdb.exceptions import InfluxDBClientError
from datetime import datetime
import sys
import csv
#import time
import argparse
import json
import pytz


metricsout = []


def get_config_value(key, default_value):
    if key in config:
        return config[key]
    return default_value

def parse_data(input_file, verbose):
    if verbose:
        print('Starting parse_data')



    point = []
    tag_values = []
    rows_generated = 0
    rows_delivered = 0
    tag = ''
    pmult = 0
    dt_format = '%Y-%m-%d %H:%M:%S'
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
                sce_timestamp = [
                    item.replace('\xa0', '') for item in sce_timestamp
                ]
                dt_local = datetime.strptime(sce_timestamp[0], dt_format)
                dt_utc = dt_local.astimezone(pytz.UTC)
                dt_utc = dt_utc.strftime("%Y-%m-%d %H:%M:%S")
                # use local time instead of UTC as you want customer month
                dt_month = dt_local.strftime('%B')
                if tag == 'generated':
                    rows_generated = rows_generated + 1
                    pmult = -1
                elif tag == 'delivered':
                    rows_delivered = rows_delivered + 1
                    pmult = 1

                point = {
                    "measurement": "kwhrs",
                    "tags": {
                        "type": tag,
                        "month": dt_month
                    },
                    "time": dt_utc,
                    "fields": {
                        "value": float(row[1]) * pmult
                    }
                }

                
                if verbose:
                    print(point)

                metricsout.append(point)

    return (rows_delivered, rows_generated)


def write_csv():
    textout = ''
    current_date = datetime.now()
    fileout = 'energy' + str(int(current_date.strftime('%Y%m%d%H%M'))) + '.csv'
    with open(fileout, 'w', encoding='UTF-8') as f:
        csv_columns = 'measurement,month,time,value'
        f.write(csv_columns)
        for data in metricsout:
            textout = '\n' + json.dumps(data)
            textout = textout.replace(
                '{"measurement": "SCE", "tags": {"type": "', '')
            textout = textout.replace('"}, "time": "', ',')
            textout = textout.replace('", "fields": {"value":', ',')
            textout = textout.replace('"month": "','')
            textout = textout.replace('", ',',')
            textout = textout.replace('}}', '')
            f.write(textout)
    print('CSV File is: ', fileout)
    return ()

def write_json():
    textout = ''
    current_date = datetime.now()
    fileout = 'energy' + str(int(current_date.strftime('%Y%m%d%H%M'))) + '.json'
    with open(fileout, 'w', encoding='UTF-8') as f:
        for data in metricsout:
            textout = '\n' + json.dumps(data)
            f.write(textout)
    print('json File is: ', fileout)
    return ()



def send_data(hostname, port, user, password,
             dbname, createdb):

    client = InfluxDBClient(hostname, port, user, password, dbname)

    if createdb:
        print('Deleting database %s' % dbname)
        client.drop_database(dbname)
        print('Creating database %s' % dbname)
        client.create_database(dbname)

    if len(metricsout) > 0:
        client.switch_user(user, password)
        response = client.write_points(metricsout, time_precision='m')

    if args.verbose:
        print('influxdb response', response)
    return ()


if __name__ == '__main__':
    config_filename = 'greenbutton.json'
    config = {}
    with open(config_filename) as configFile:
        config = json.load(configFile)

    parser = \
        argparse.ArgumentParser(description="""Loads Green Button csv file
        and send formated results to influxdb. 
        Used for Net Metering format only (solar)"""
                               )
    parser.add_argument('--version',
                        help='display version number',
                        action='store_true')
    parser.add_argument(
        '-f',
        '--file',
        required=True,
        help='*REQUIRED* filename of the utility provided csv kwh file')
    parser.add_argument(
        '-v',
        '--verbose',
        help='verbose output - send copy of each line to stdout',
        action='store_true')
    parser.add_argument('-q',
                        '--quiet',
                        help='do not print totals output',
                        action='store_true')
    parser.add_argument(
        '-c',
        '--csv',
        help='sends parsed data to a csv delimited file',
        action='store_true')
    parser.add_argument(
        '-j',
        '--json',
        help='sends parsed data to a json file',
        action='store_true')
    parser.add_argument(
        '--createdb',
        action='store_true',
        default=False,
        help='Drop database and create a new one')
    parser.add_argument(
        '--nodb',
        action='store_true',
        default='False',
        help='Will NOT import to influxdb. Use with -o for local file only'
    )
    args = parser.parse_args()

    if args.version:
        print('sceinfluxdb.py - version', __version__)
        sys.exit()

    (delivered, generated) = parse_data(args.file, args.verbose)

    if args.csv:
        write_csv()

    if args.json:
        write_json()

    #if not args.nodb:
    send_data(config['host'], config['port'], config['user'],
             config['password'], config['dbname'], args.createdb)

    if args.verbose:
        print('Influx Host:', config['host'])
        print('Influx Port:', config['port'])

    if not args.quiet:
        print('Import Complete')
        print('Energy Delivered rows ', delivered)
        print('Energy Generated rows ', generated)
sys.exit()
