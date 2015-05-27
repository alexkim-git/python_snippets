#-------------------------------------------------------------------------------
# Name:
# Purpose:
# Author:      Alexander Kim
# Created:
# Version:
#-------------------------------------------------------------------------------
import os
import csv
from get_region_country_name import get_region_country_name
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

lat_lon=[]
region_name=[]
print 'lat', 'lon', 'region'
with open(f, 'rb') as csvfile:
    csvreader = csv.reader(csvfile)
    for i,row in enumerate(csvreader):
        try:
            lat=float(row[0])
            lon=float(row[1])
            region=get_region_country_name(lat,lon,'akim_urthecast')
            print lat, lon, region
            region_name.append(region)
            lat_lon.append([lat,lon])
        except:
            print 'Error parsing values in line %s in csv: %s' %(str(i+1),row)
            pass

output_file=output_folder+'out_'+file_name
with open(output_file, 'wb') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Lat','Lon','Region'])
    for lat_lon,region in zip(lat_lon,region_name):
        lat=lat_lon[0]
        lon=lat_lon[1]
        csvwriter.writerow([lat,lon,region])

print 'Output file has been placed to %s' %output_file
