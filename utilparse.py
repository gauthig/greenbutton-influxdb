#utilparse.py
#module to parse all metrics based on utility format
#Notes
#  UNIX timestamp for influxdb converted to UTC - grafana will convert back to local
#  tags are using local (input file) time zone
#
#  Interval times are end times only, start is assumed in a timebased database

from datetime import datetime
import csv
import pytz
import re

rows_generated = 0
rows_delivered = 0

def parse_data(input_file, verbose, util_format, metricsout):
    if verbose:
        print('Starting parse_data')

    infile = open(input_file, mode='r')
    csv_reader = csv.reader(infile, delimiter=',')
    if verbose:
        print('File: ', infile)

    if util_format == 'sce-tou':
        sce_tou_parse(csv_reader, verbose, metricsout)
    elif util_format == 'pep':
        pep_parse(csv_reader, verbose, metricsout)
    return (rows_delivered, rows_generated, metricsout)


def sce_tou_parse(csv_reader, verbose, metricsout):
    global rows_generated
    global rows_delivered
    point = []
    tag = ''
    pmult = 0

    for row in csv_reader:
        if len(row) > 0:
            if 'Received' in row[0]:
                tag = 'generated'
            elif 'Delivered' in row[0]:
                tag = 'delivered'
            elif 'Consumption' in row[0]:
                tag = 'delivered'
            elif 'to' in row[0]:
                util_timestamp = row[0].split('to')
                # SCE adds non-ASCII charter before the to field, need to strip
                util_timestamp = [
                    item.replace('\xa0', '') for item in util_timestamp
                ]
                dt_local = datetime.strptime(util_timestamp[0], '%Y-%m-%d %H:%M:%S')
                dt_utc = dt_local.astimezone(pytz.UTC)
                dt_utc = dt_utc.strftime("%Y-%m-%d %H:%M:%S")
                # use local time instead of UTC as you want customer month
                if float(row[1]) != 0:
                    if tag == 'generated':
                        rows_generated = rows_generated + 1
                        pmult = -1
                    elif tag == 'delivered':
                        rows_delivered = rows_delivered + 1
                        pmult = 1
        
                    point = {
                        "measurement": "energy",
                        "tags": {
                            "type": tag,
                            "month": dt_local.strftime('%B'),
                            "day": dt_local.strftime('%A'),
                            "year": dt_local.strftime('%Y'),
                        },
                        "time": dt_utc,
                        "fields": {
                            "kwh": float(row[1]) * pmult
                        }
                    }

                if verbose:
                    print(point)

                metricsout.append(point)

def pep_parse(csv_reader, verbose, metricsout):
    global rows_generated
    global rows_delivered
    point = []
    tag = ''

    for row in csv_reader:
        if len(row) > 0:
            if 'Electric usage' in row[0]:
                if float(row[4]) < 0:
                    tag = 'generated'
                else:
                    tag = 'delivered'

                util_timestamp = row[1]
                util_timestamp = str(util_timestamp) + ' ' + str(row[3]) + str(':00')
                dt_local = datetime.strptime(util_timestamp, "%Y-%m-%d %H:%M:%S")
                dt_utc = dt_local.astimezone(pytz.UTC)
                dt_utc = dt_utc.strftime("%Y-%m-%d %H:%M:%S")
                # use local time instead of UTC as you want customer month

                if tag == 'generated':
                    rows_generated = rows_generated + 1
                    cost = float(re.sub(r'[^0-9]', '', row[6]))/-100
                elif tag == 'delivered':
                    rows_delivered = rows_delivered + 1
                    cost = float(re.sub(r'[^0-9]', '', row[6]))/100

                point = {
                    "measurement": "energy",
                    "tags": {
                        "type": tag,
                        "month": dt_local.strftime('%B'),
                        "day": dt_local.strftime('%A'),
                        "year": dt_local.strftime('%Y'),
                    },
                    "time": dt_utc,
                    "fields": {
                        "kwh": float(row[4]),
                        "cost" : cost
                    }
                }

                if verbose:
                    print(point)

                metricsout.append(point)

    return ()
