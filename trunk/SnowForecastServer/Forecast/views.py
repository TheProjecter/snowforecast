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
    f = open("Prueba.txt",'w')
    while(index < (nLines-1)):
        f.write(str(index))
        f.write(" "+page[index]+'\n')
        if re.match('   <table class="forecasts"> ', page[index]):
            print index, page[index]
        index+=1
    f.close()
    # Return XML Conversion
    return HttpResponse("OK", status=200)
