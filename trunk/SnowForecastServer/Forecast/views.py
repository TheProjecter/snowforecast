from django.http import HttpResponse
import urllib, httplib
from urlparse import urlparse
import re



# Function that transform the html
def XMLSnowForecast(request):

    if not request.GET.has_key('url'):
        return HttpResponse("BAD PARAMS", status=400)

    # Get html file of the forecast of the ski-resort specified in the URL
    url = request.GET['url']
    proto, host, cgi = urlparse(url)[:3]
    conn = httplib.HTTPConnection(host)
    conn.request('GET', cgi)
    response = conn.getresponse()

    page = response.read()
    page = page.split('\n')
    
    index = 0
    nLines = len(page)
    days = {}
    patternColor = re.compile('.*<td bgcolor="(?P<color>.+)" class="cell">.*')
    patternDay = re.compile('.*<b>(?P<day>.+)</b>.*')
    patternDayNumer = re.compile('.*<div class="dom">(?P<dayNumber>.+)</div>.*')

    while(index < (nLines-1)):


        # Search table that have the forecast of the ski-resort
        if re.match('.*<table class="forecasts">.*', page[index]):
            
            # Read the table
            while(not (re.match('.*</table>.*', page[index]))):

                # Get color background days
                if patternColor.search(page[index]):
                    result = patternColor.search(page[index])
                    color = result.group('color')

                # Get name day
                if patternDay.search(page[index]):
                    result = patternDay.search(page[index])
                    
                    
                # Search the follow line
                index+=1
 
        index+=1

    # Return XML Conversion
    return HttpResponse("OK", status=200)
