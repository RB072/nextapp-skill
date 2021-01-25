from mycroft import MycroftSkill, intent_file_handler
import caldav
from configparser import ConfigParser

file = 'config.ini'
config = ConfigParser()
config.read(file)
from caldav.elements import dav
from datetime import datetime, timedelta, time
today  = datetime.combine(datetime.today(), time(0,0))
# Caldav url
# Works on both Win or LinuxS

username = config['user']['_siNextcloudUser']
password = config['user']['_siNextcloudPW']

url = "https://" + username + ":" + password + "@next.social-robot.info/nc/remote.php/dav"
# open connection to calendar
client = caldav.DAVClient(url)
principal = client.principal()
# get all available calendars (for this user)
calendars = principal.calendars()

# check the calendar events and parse results..

if len(calendars) > 0:
  calendar = calendars[0]
  events = calendar.date_search(today, datetime.combine(today, time(23,59,59,59))) #Events am heutigen Tag

  if len(events) == 0:
    print("No events today!")
  else:
    print("Total {num_events} events:".format(num_events=len(events)))

    for event in events:
      event.load()
      e = event.instance.vevent
      if e.dtstart.value.strftime("%H:%M") == "00:00":
        # Überprüfung von ganztägigen Events
        eventTime = e.dtstart.value.strftime("%D")
        print("{eventTime} {eventSummary}".format(eventTime=eventTime, eventSummary=e.summary.value))
        caldavAppointment="{eventTime} {eventSummary}".format(eventTime=eventTime, eventSummary=e.summary.value) ## Unsere Aufruf Variabel
      else:
        # This is a "normal" event
        eventTime = e.dtstart.value.strftime("%H:%M")
        print("{eventTime} {eventSummary})".format(eventTime=eventTime, eventSummary=e.summary.value))

class Nextapp(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('nextapp.intent')
    def handle_nextapp(self, message):
        try:
            if len(calendars) > 0:
                calendar = calendars[0]
                events = calendar.date_search(today,
                                              datetime.combine(today, time(23, 59, 59, 59)))  # Events am heutigen Tag

                if len(events) == 0:
                    print("No events today!")
                else:
                    print("Total {num_events} events:".format(num_events=len(events)))

                    for event in events:
                        event.load()
                        e = event.instance.vevent
                        if e.dtstart.value.strftime("%H:%M") == "00:00":
                            # Überprüfung von ganztägigen Events
                            eventTime = e.dtstart.value.strftime("%D")
                            print(
                                "{eventTime} {eventSummary}".format(eventTime=eventTime, eventSummary=e.summary.value))
                            caldavAppointment = "{eventTime} {eventSummary}".format(eventTime=eventTime,eventSummary=e.summary.value)  ## Unsere Aufruf Variabel
                            response = {'apptoday': caldavAppointment}
                            self.speak_dialog('nextapp', data=response)
                        else:
                            # This is a "normal" event
                            eventTime = e.dtstart.value.strftime("%H:%M")
                            print(
                                "{eventTime} {eventSummary})".format(eventTime=eventTime, eventSummary=e.summary.value))


        except:
            self.speak_dialog("no_event")


def create_skill():
    return Nextapp()

