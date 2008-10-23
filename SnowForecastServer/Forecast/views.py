from django.http import HttpResponse
import urllib, httplib
from urlparse import urlparse
import re
import Tables
from django.template import loader, Context

   
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
    patternFirstLine = re.compile('.*<tr class="lar hea">.*')
    patternPictureLine = re.compile('.*<tr class="icons">.*')
    patternStartLine = re.compile('.*<tr>.*')
    patternSummaryLine = re.compile('.*<tr class="med sum">.*')
    patternSnowLine = re.compile('.*<tr class="lar">.*')
    patternFreezingLine = re.compile('.*<tr class="lar fl">.*')

    finLine = re.compile('.*</tr>.*')
    finTable = re.compile('.*</table>.*')
    line = []
    pictureLine = []
    firtsLine = []
    pictureWindLine = []
    rainLine = []
    snowLine = []
    maxLine = []
    minLine = []
    sensationLine = []
    freezingLine = []

    while(index < (nLines-1)):


        # Search table that have the forecast of the ski-resort
        if re.match('.*<table class="forecasts">.*', page[index]):

            while(not (finTable.search(page[index])) and (index < nLines-1)):

                # Read the first line
                if(patternFirstLine.search(page[index])):
                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1

                    color, day, dayNumber, time = Tables.GetFirtsLine(line)
                
                # Get the weather icons
                if(patternPictureLine.search(page[index])):
                    line = []
                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1
                    
                    pictureLine = Tables.GetPictureLine(line)

                # Get the wind icons
                if(patternStartLine.search(page[index])):
                    line = []
                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1
                    if ((pictureLine != []) and (pictureWindLine == [])):
                        pictureWindLine = Tables.GetWindLine(line)

                # Get the summary wheather
                if(patternSummaryLine.search(page[index])):
                    line = []
                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1
                    summaryLine = Tables.GetSummaryLine(line)

                # Get the snow cm
                if(patternSnowLine.search(page[index]) and (snowLine == [])):
                    line = []
                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1
                    snowLine = Tables.GetSnowLine(line)

                # Get the rain cm
                if(patternSnowLine.search(page[index]) and (rainLine == [])):
                    line = []

                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1

                    rainLine = Tables.GetRainLine(line)

                # Get the max temperature
                if((patternSnowLine.search(page[index])) and (maxLine == [])):
                    line = []

                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1

                    maxLine = Tables.GetMaxLine(line)

                # Get the min temperature
                if((patternSnowLine.search(page[index])) and (minLine == [])):
                    line = []

                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1

                    minLine = Tables.GetMinLine(line)

                # Get the sensation temperature
                if((patternSnowLine.search(page[index])) and (sensationLine == [])):
                    line = []

                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1

                    sensationLine = Tables.GetSensationLine(line)

                if(patternFreezingLine.search(page[index]) and (freezingLine == [])):
                    line = []
                    while(not finLine.search(page[index])):
                        line.append(page[index])
                        index+=1

                    freezingLine = Tables.GetFreezingLine(line)
      
                index+=1
        index+=1
    # Return XML Conversion
#    t = loader.get_template('template/xmlConversion.xml')
#    c = Context({'days':days,'daysNumber':daysNumber,'time':time,'picture':pictureLine,'wind':pictureWindLine,
#                 'summary':summaryLine,'snow':snowLine,'rain':rainLine, 'maxs':maxLine, 'mins':minLine, 'sensations':sensationLine,
#                 'freezing':freezingLine})
                 
#    return HttpResponse(t.render(c), status=200, mimetype='text/xml')
