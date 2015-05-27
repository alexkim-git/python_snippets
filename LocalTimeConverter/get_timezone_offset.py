# -------------------------------------------------------------------------------
# Author:      Alexander Kim
# -------------------------------------------------------------------------------
from urllib2 import urlopen
import json
import datetime
import calendar


def ut(d): return calendar.timegm(d.timetuple())


def get_timezone_offset(lat, lon, utc_time):
    try:
        api_key = "" #You Google API key Here
        url = 'https://maps.googleapis.com/maps/api/timezone/json?location=%s,%s&timestamp=%s&key=%s' % (lat, lon, ut(utc_time), api_key)
        jsonurl = urlopen(url)
        data = json.loads(jsonurl.read())
        dstOffset = data['dstOffset']
        rawOffset = data['rawOffset']
        gmtOffset = (dstOffset + rawOffset) / 3600.0
        timeZoneId = data['timeZoneId']
        print utc_time, lat, lon, float(gmtOffset), timeZoneId
        return float(gmtOffset), timeZoneId
    except Exception as ex:
        print "Error: %s" %ex
        print utc_time, lat, lon, "NA", "NA"
        return "NA", "NA"

if __name__ == "__main__":
    lat = '49.288553'
    lon = '-123.137818'
    utc_time = datetime.datetime(2015, 3, 10, 9)
    print get_timezone_offset(lat, lon, utc_time)
