#-------------------------------------------------------------------------------
# Author:      Alexander Kim
#-------------------------------------------------------------------------------
import os
import csv
import datetime
from get_cloud_cover import get_cloud_cover
input_folder='Input/'
output_folder='Output/'
input_file_names=[]
for path, subdirs, files in os.walk(input_folder):
    for name in files:
        if name[0].isalnum() and name.endswith('.csv'):
            input_file=os.path.join(path, name).replace('\\','/')
            input_file_names.append(input_file)

for i,input_file in enumerate(input_file_names):
    print '%s - %s' %(i,input_file)

file_num=int(raw_input('Choose input file:'))
f=input_file_names[file_num]
file_name=f.replace(input_folder,'')

times=[]
lat_lon=[]
cloud_scores=[]

with open(f, 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for i,row in enumerate(csvreader):
        try:
            utc_tm=datetime.datetime.strptime(row[0], '%Y-%m-%dT%H:%M:%SZ')
            lat=float(row[1])
            lon=float(row[2])
            cloud_cover=get_cloud_cover(utc_tm,lat,lon)
            times.append(utc_tm)
            cloud_scores.append(cloud_cover)
            lat_lon.append([lat,lon])
        except:
            print 'Error parsing values in line %s in csv: %s' %(str(i+1),row)
            pass

output_file=output_folder+'out_'+file_name
with open(output_file, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    print 'Time','Lat','Lon','Cloud Cover %'
    csvwriter.writerow(['Time','Lat','Lon','Cloud Cover %'])
    for utc_tm,lat_lon,cloud_score in zip(times,lat_lon,cloud_scores):
        lat=lat_lon[0]
        lon=lat_lon[1]
        if cloud_score is not None:
            csvwriter.writerow([utc_tm.strftime('%Y-%m-%dT%H:%M:%SZ'),lat,lon,cloud_score*100])
            print utc_tm.strftime('%Y-%m-%dT%H:%M:%SZ'),lat,lon,cloud_score*100
        else:
            csvwriter.writerow([utc_tm.strftime('%Y-%m-%dT%H:%M:%SZ'),lat,lon,'N/A'])
            print utc_tm.strftime('%Y-%m-%dT%H:%M:%SZ'),lat,lon,'N/A'
print 'Output file has been placed to %s' %output_file
