#-------------------------------------------------------------------------------
# Author:      Alexander Kim
#-------------------------------------------------------------------------------

def get_cloud_cover(utc_tm,lat,lon):
    from urllib2 import urlopen
    import urllib
    import json
    import calendar
    import datetime
    iso_tm=utc_tm.strftime('%Y-%m-%dT%H:%M:%SZ')
    forecast_url='https://api.forecast.io/forecast/YOUR_API_KEY_HERE/%s,%s,%s' %(lat,lon,iso_tm)
    try:
        jsonurl = urlopen(forecast_url)
        data = json.loads(jsonurl.read())
        cloud_cover=data['currently']['cloudCover']
    except:
        cloud_cover=None
    return cloud_cover

'''
import datetime
lat='54.291993'
lon='-123.130013'
utc_tm=datetime.datetime(2014,6,30,12,43,24)
print get_cloud_cover(utc_tm,lat,lon)
'''
