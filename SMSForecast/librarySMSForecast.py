try:
  from xml.etree import ElementTree # for Python 2.5 users
except ImportError:
  from elementtree import ElementTree
import gdata.calendar.service
import gdata.service
import atom.service
import gdata.calendar
import atom
import getopt
import sys
import string
import time
import re
import settings
import urllib, httplib
from urlparse import urlparse
from xml.dom.minidom import parse, parseString


#Login in google calendar
def Login(user, password):
    calendar_service = gdata.calendar.service.CalendarService()
    calendar_service.email = user
    calendar_service.password = password
    calendar_service.source = 'Google-Calendar_SnowCalendar-1.0'
    calendar_service.ProgrammaticLogin()
    return calendar_service


# Check if calendar is created
def ExistCalendar(calendar_service, calendar):
  feed = calendar_service.GetAllCalendarsFeed()
  for i, a_calendar in enumerate(feed.entry):
    if(calendar == a_calendar.title.text):
        return True
  return False

# Retrieving only calendar that a user owns
def PrintOwnCalendars(calendar_service):
  feed = calendar_service.GetOwnCalendarsFeed()
  print feed.title.text
  for i, a_calendar in enumerate(feed.entry):
    print '\t%s. %s %s' % (i, a_calendar.title.text,a_calendar.GetEditLink().href)
    #print dir(a_calendar)


# Get uri of the calendar
def GetIDCalendar(calendar_service, calendar):
  feed = calendar_service.GetOwnCalendarsFeed()
  for i, a_calendar in enumerate(feed.entry):
    if(calendar == a_calendar.title.text):
        pattern = re.compile("http://www.google.com/calendar/feeds/default/owncalendars/full/(?P<IDCalendar>.+)")
        result = pattern.search(a_calendar.GetEditLink().href)
        return result.group('IDCalendar')


# Create new calendar
def CreateCalendar(calendar_service, calendarName):
    # Create the calendar
    calendar = gdata.calendar.CalendarListEntry()
    calendar.title = atom.Title(text=calendarName)
    calendar.summary = atom.Summary(text='This calendar contains snow forecast events')
    calendar.where = gdata.calendar.Where(value_string='Spain')
    calendar.color = gdata.calendar.Color(value='#2952A3')
    calendar.timezone = gdata.calendar.Timezone(value='Europe/Madrid')
    calendar.hidden = gdata.calendar.Hidden(value='false')
    new_calendar = calendar_service.InsertCalendar(new_calendar=calendar)
    return new_calendar


# Insert Single Event in the calendar
def InsertSingleEvent(calendar_service, title='One-time Tennis with Beth', 
                      content='Meet for a quick lesson', where='On the courts',
                      IDCalendar='default', start_time=None, end_time=None):
    event = gdata.calendar.CalendarEventEntry()
    event.title = atom.Title(text=title)
    event.content = atom.Content(text=content)
    event.where.append(gdata.calendar.Where(value_string=where))

    if start_time is None:
      # Use current time for the start_time and have the event last 1 hour
      start_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + 600))
      end_time = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time() + (4200)))
    event.when.append(gdata.calendar.When(start_time=start_time, end_time=end_time))
    
    new_event = calendar_service.InsertEvent(event, '/calendar/feeds/'+IDCalendar+'/private/full')
    
    #print 'New single event inserted: %s' % (new_event.id.text,)
    #print '\tEvent edit URL: %s' % (new_event.GetEditLink().href,)
    #print '\tEvent HTML URL: %s' % (new_event.GetHtmlLink().href,)
    return new_event


# Quick add a new event
def quick_add(calendar_service, text ,IDCalendar):
    event = gdata.calendar.CalendarEventEntry()
    event.content = atom.Content(text=text)
    event.quick_add = gdata.calendar.QuickAdd(value='true')    
    # Send the request and receive the response:
    new_event = calendar_service.InsertEvent(event, '/calendar/feeds/'+IDCalendar+
                                             '/private/full')
    return new_event


# Print all events on default Calendar
def PrintAllEventsOnDefaultCalendar(calendar_service):
  feed = calendar_service.GetCalendarEventFeed()
  print 'Events on Primary Calendar: %s' % (feed.title.text,)
  for i, an_event in enumerate(feed.entry):
    print '\t%s. %s' % (i, an_event.title.text,)
    for p, a_participant in enumerate(an_event.who):
      print '\t\t%s. %s' % (p, a_participant.email,)
      print '\t\t\t%s' % (a_participant.name,)
      print '\t\t\t%s' % (a_participant.attendee_status.value,)


# Add reminder or notifcations in a event by SMS
def AddReminder(calendar_service, event, minutes=5):
  for a_when in event.when:
    if len(a_when.reminder) > 0:
      a_when.reminder[0].minutes = minutes
    else:
      a_when.reminder.append(gdata.calendar.Reminder(minutes=minutes))

  #print 'Adding %d minute reminder to event' % (minutes,)
  return calendar_service.UpdateEvent(event.GetEditLink().href, event)


# Get summary reports week
def GetSummarySnowReport(listDay, listDayNumber, listSnowCm, 
                           listMax, listMin, listFreezing):
  listReport = []
  day = listDay[0]
  dayNumber = listDayNumber[0]
  cm = 0
  max = listMax[0]
  min = listMin[0]
  freezingMin = listFreezing[0]
  freezingMax = listFreezing[0]

  for i in range(len(listDay)-1):
    
    if(dayNumber == listDayNumber[i]):
      if(listSnowCm[i] != str('-')):
        cm+= int(listSnowCm[i])
      if(max < listMax[i]):
        max = listMax[i]
      if(min > listMin[i]):
        min = listMin[i]
      if(freezingMin > listFreezing[i]):
        freezingMin = listFreezing[i]
      if(freezingMax < listFreezing[i]):
        freezingMax = listFreezing[i]

    else:
      if (cm > 0):
        listReport.append((daysInitial(day), dayNumber, cm, max, min, freezingMin, freezingMax))

      dayNumber = listDayNumber[i]
      day = listDay[i]
      if(listSnowCm[i] != '-'):
        cm = int(listSnowCm[i])
      else:
        cm = 0
        max = listMax[i]
        min = listMin[i]
        freezingMin = listFreezing[i]
        freezingMax = listFreezing[i]

  if (cm > 0):
    listReport.append((daysInitial(day), dayNumber, cm, max, min, freezingMin, freezingMax))
  return listReport


# Return initial day
def daysInitial(day):
  if (day == 'Mon'):
    return 'L'
  if (day == 'Tue'):
    return 'M'
  if (day == 'Wed'):
    return 'X'
  if (day == 'Thu'):
    return 'J'
  if (day == 'Fri'):
    return 'V'
  if (day == 'Sat'):
    return 'S'
  if (day == 'Sun'):
    return 'D'
  return 'L'


# Get the reports of snow forecast in the ski resorts specified in file settings.
def GetReports(url):
  listReports = []
  
  url = settings.SERVER+url+settings.XML_FORECAST
  proto, host, cgi = urlparse(url)[:3]
  conn = httplib.HTTPConnection(host)
  conn.request('GET', cgi)
  response = conn.getresponse()

  xml = parseString(response.read())
  # Get the list days
  listDay = []
  for day in xml.getElementsByTagName('DAYNAME'):
    listDay.append(day.childNodes[0].nodeValue)

  # Get the number day
  listDayNumber = []
  for day in xml.getElementsByTagName('DAYNUMBER'):
    listDayNumber.append(int(day.childNodes[0].nodeValue))

  # Get the list snow cm
  listSnowCm = []
  for day in xml.getElementsByTagName('SNOW'):
    listSnowCm.append(day.childNodes[0].nodeValue)
    

  listMax = []
  # Get the max temperature
  for day in xml.getElementsByTagName('MAXTEMP'):
      listMax.append(int(day.childNodes[0].nodeValue))

  # Get the min temperature
  listMin = []
  for day in xml.getElementsByTagName('MAXTEMP'):
      listMin.append(int(day.childNodes[0].nodeValue))

  # Get Freezing Level
  listFreezing = []
  for day in xml.getElementsByTagName('FREEZING'):
      listFreezing.append(int(day.childNodes[0].nodeValue))

  listReports = GetSummarySnowReport(listDay, listDayNumber, listSnowCm, 
                           listMax, listMin, listFreezing)
  return listReports
  

      
