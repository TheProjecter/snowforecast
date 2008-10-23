import re

# Get the information of the firts line
def GetFirtsLine(lines):
    columns = {}
    patternColor = re.compile('.*<td bgcolor="(?P<color>.+)" class="cell">.*')
    patternDay = re.compile('.*<b>(?P<day>.+)</b>.*')
    patternDayNumber = re.compile('.*<div class="dom">(?P<dayNumber>.+)</div>.*')
    firtsDay = 31
    finalDay = 0
    list = []
    time = []

    for line in lines:
        if (patternColor.search(line)):
            result = patternColor.search(line)
            color = result.group('color')

        if (patternDay.search(line)):
            result = patternDay.search(line)
            day = result.group('day')

        if (patternDayNumber.search(line)):
            result = patternDayNumber.search(line)
            dayNumber = result.group('dayNumber')
            list.append({'day':day,'dayNumber':dayNumber,'color':color})
            if (int(dayNumber)> (finalDay)):
                finalDay = int(dayNumber)

            if (int(dayNumber) < firtsDay):
                firtsDay = int(dayNumber)

            if columns.has_key(day):
                color, dayNumber, n = columns[day]
                n+=1
                columns[day]=(color, int(dayNumber), n)
            else:
                columns[day]=(color, int(dayNumber), 1)
        

    for index in columns.keys():
        color, dayNumber, n = columns[index]
        
        if dayNumber == firtsDay:
            if (n == 3):
                columns[index] = (color, dayNumber, ["Morning", "Afternoon", "Night"])
                time = time + ["Morning", "Afternoon", "Night"]        
            if (n == 2):
                columns[index] = (color, dayNumber, ["Afternoon", "Night"])
                time = time + ["Afternoon", "Night"]
            if (n == 1):
                columns[index] = (color, dayNumber, ["Night"])
                time = time + ["Night"]
        
        elif dayNumber == finalDay:
            if (n == 3):
                columns[index] = (color, dayNumber, ["Morning", "Afternoon", "Night"])
                time = time + ["Morning", "Afternoon", "Night"]
            if (n == 2):
                columns[index] = (color, dayNumber, ["Morning", "Afternoon"])
                time = time + ["Morning", "Afternoon"]
            if (n == 1):
                columns[index] = (color, dayNumber, ["Morning"])
                time = time + ["Morning"]
        else:
            columns[index] = (color, dayNumber, ["Morning", "Afternoon", "Night"])
            time = time + ["Morning", "Afternoon", "Night"]

    for index in list:
        index['time'] = time[0]
        time.remove(time[0])

    print list
    return list, time


# Get the information of the second line. Get the uri of the pictures in snowforecast
def GetPictureLine(lines):
    patternPicture = re.compile('.*src="(?P<url>.+)" alt="".*')
    icons = []
    for line in lines:
        if(patternPicture.search(line)):
            result = patternPicture.search(line)
            icons.append('http://www.snow-forecast.com'+result.group('url'))
    
    return icons

# Get the wind icons
def GetWindLine(lines):
    patternWind = re.compile('.*src="(?P<url>.+)" alt=""/>')
    icons = []
    for line in lines:
        if(patternWind.search(line)):
            result = patternWind.search(line)
            icons.append('http://www.snow-forecast.com'+result.group('url'))
    return icons

# Get the weather summary
def GetSummaryLine(lines):
    patternSummary = re.compile('.*<td>(?P<summary>.+)</td>.*')
    summary = []
    for line in lines:
        if(patternSummary.search(line)):
            result = patternSummary.search(line)
            summary.append(result.group('summary'))

    return summary

#Get the snow line
def GetSnowLine(lines):
    patternSnow = re.compile('.*<b><span class="snow">(?P<snowcm>.+>)</.*')
    snow = []
    for line in lines:

        if(patternSnow.search(line)):
            result = patternSnow.search(line)
            snow.append(result.group('snowcm').split('</span></b>')[0])

    return snow

#Get the snow line
def GetRainLine(lines):
    patternRain = re.compile('.*<b><span class="rain">(?P<rainmm>.+>)</.*')
    rain = []
    for line in lines:

        if(patternRain.search(line)):
            result = patternRain.search(line)
            rain.append(result.group('rainmm').split('</span></b>')[0])

    return rain

# Get the max line
def GetMaxLine(lines):
    patternTemp = re.compile('.*<span class="temp">(?P<temp>.+>)')
    patternColor = re.compile('.*<td bgcolor="(?P<color>.+)">.*')
    temp = []
    for line in lines:
        if(patternColor.search(line)):
            result = patternColor.search(line)
            color = result.group('color')
        if(patternTemp.search(line)):
            result = patternTemp.search(line)
            temp.append({'color':color, 'temp':result.group('temp').split('</span>')[0]})
    return temp


# Get the min line
def GetMinLine(lines):
    patternTemp = re.compile('.*<span class="temp">(?P<temp>.+>)')
    patternColor = re.compile('.*<td bgcolor="(?P<color>.+)">.*')
    temp = []
    for line in lines:
        if(patternColor.search(line)):
            result = patternColor.search(line)
            color = result.group('color')
        if(patternTemp.search(line)):
            result = patternTemp.search(line)
            temp.append({'color':color, 'temp':result.group('temp').split('</span>')[0]})
    return temp

# Get the sensation termic
def GetSensationLine(lines):
    patternTemp = re.compile('.*<span class="temp">(?P<temp>.+>)')
    temp = []
    for line in lines:
        if(patternTemp.search(line)):
            result = patternTemp.search(line)
            temp.append(result.group('temp').split('</span>')[0])            
    return temp

# Get the sensation termic
def GetFreezingLine(lines):
    patternFreezing = re.compile('.*<span class="heightfl">(?P<height>.+>)')
    freezing = []
    for line in lines:
        if(patternFreezing.search(line)):
            result = patternFreezing.search(line)
            freezing.append(result.group('height').split('</span>')[0])

    return freezing
