__author__ = 'akim'
import datetime
import os
import csv
import time
from get_timezone_offset import get_timezone_offset

input_folder = 'Input/'
output_folder = 'Output/'
input_file_names = []
for path, subdirs, files in os.walk(input_folder):
    for name in files:
        if name[0].isalnum() and name.endswith('.csv'):
            input_file = os.path.join(path, name).replace('\\', '/')
            input_file_names.append(input_file)

for i, input_file in enumerate(input_file_names):
    print '%s - %s' % (i, input_file)

file_num = int(raw_input('Choose input file:'))
f = input_file_names[file_num]
file_name = f.replace(input_folder, '')

times = []
lat_lon = []
time_offsets = []
timezones = []

with open(f, 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for i, row in enumerate(csvreader):
        if i>0:
            time.sleep(0.1)
            utc_tm = datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%SZ')
            lat = float(row[1])
            lon = float(row[2])
            tm_offset, timezoneId = get_timezone_offset(lat, lon, utc_tm)
            times.append(utc_tm)
            time_offsets.append(tm_offset)
            timezones.append(timezoneId)
            lat_lon.append([lat, lon])


i = 1
output_file = output_folder + 'out_' + file_name
with open(output_file, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    print 'Time', 'Lat', 'Lon', 'Time Offset', 'Time Zone ID'
    csvwriter.writerow(['Time', 'Lat', 'Lon', 'Time Offset', 'Time Zone ID'])
    for utc_tm, lat_lon, tm_offset, timezoneId in zip(times, lat_lon, time_offsets, timezones):
        lat = lat_lon[0]
        lon = lat_lon[1]
        csvwriter.writerow([utc_tm.strftime('%Y-%m-%dT%H:%M:%SZ'), lat, lon, tm_offset, timezoneId])
        print "%s), %s, %s, %s, %s, %s" %(i, utc_tm.strftime('%Y-%m-%dT%H:%M:%SZ'), lat, lon, tm_offset, timezoneId)
        i = i + 1

print 'Output file has been placed to %s' % output_file

