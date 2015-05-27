#-------------------------------------------------------------------------------
# Author:      Alexander Kim
#-------------------------------------------------------------------------------

def get_region_country_name(lat,lon,username):
    import xml.etree.ElementTree as ET
    from urllib2 import urlopen
    import unicodedata
    geonames_url='http://api.geonames.org/countrySubdivision?lat=%s&lng=%s&username=%s' %(lat,lon,username)
    xmlurl = urlopen(geonames_url)
    tree = ET.parse(xmlurl)
    root = tree.getroot()
    try:
        country=unicode(root[0][1].text)
        country=unicodedata.normalize('NFKD', country).encode('ascii','ignore')
        try:
            region=unicode(root[0][3].text)
            region=unicodedata.normalize('NFKD', region).encode('ascii','ignore')
            return '%s, %s' %(region,country)
        except:
            return country
    except:
        return 'N/A'

