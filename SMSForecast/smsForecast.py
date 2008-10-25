from librarySMSForecast import *
import sys
import settings
#Nos autenticamos en el calendario

#Show the help and a case use.
def help():
  print "Add new forecast events in a google calendar. Add Notifications of those events by SMS."
  print "Use: python smsForecast.py --user [username] --pw [password] --cl [calendar]"


# Check the arguments
if(len(sys.argv) < 7):
  help()
  exit()

#Login in the google calendar 
calendar_service = Login(sys.argv[2], sys.argv[4])

# Check if calendar is created
if (not ExistCalendar(calendar_service, sys.argv[6])):
  # Create new calendar if not it was created
  calendar = CreateCalendar(calendar_service, sys.argv[6])

# Get the snow forecast of the ski resort.
for resort in settings.SKI_RESORTS.keys():
  reports = GetReports(settings.SKI_RESORTS[resort])

  # Add event in google calendar if will snow
  if (reports != []):
    title = ""
    for reportDay in reports:
      day, dayNumber, cm, max, min, freezingMin, freezingMax = reportDay
      if (reportDay != reports[len(reports)-1]):
        title += day + str(dayNumber) + ":" + str(cm) + "cm["+str(min) + "," + str(max) + "]" + str(freezingMin) + "m,"   
      else:
        title += day + str(dayNumber) + ":" + str(cm) + "cm["+str(min) + "," + str(max) + "]" + str(freezingMin) + "m,"


    IDCalendar = GetIDCalendar(calendar_service, sys.argv[6])
    event = InsertSingleEvent(calendar_service, title, 
                              title, 
                              resort,
                              IDCalendar, 
                              start_time=None, 
                              end_time=None)
    AddReminder(calendar_service, event, 5)


