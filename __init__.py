from mycroft import MycroftSkill, intent_file_handler
import caldav
import os
from caldav.elements import dav
from datetime import datetime, timedelta, time
today  = datetime.combine(datetime.today(), time(0,0))
# Caldav url
# Works on both Win or LinuxS
username = os.environ.get('_siNextcloudUser')
password = os.environ.get('_siNextcloudPW')
url = "https://" + username + ":" + password + "@next.social-robot.info/nc/remote.php/dav"
# open connection to calendar
client = caldav.DAVClient(url)
principal = client.principal()
# get all available calendars (for this user)
calendars = principal.calendars()
# check the calendar events and parse results..
'''if len(calendars) > 0:
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
        print("{eventTime} {eventSummary})".format(eventTime=eventTime, eventSummary=e.summary.value))'''
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
                        #Abfragen der aktuellen Zeit und der Eventzeit
                        eventTime = e.dtstart.value.strftime("%H:%M")
                        aktuelleZeit = datetime.now().strftime("%H:%M")
                        if aktuelleZeit > eventTime:
                            print(
                                "{eventTime} {eventSummary}".format(eventTime=eventTime, eventSummary=e.summary.value))
                            nextAppointmentValue = "{eventTime} {eventSummary}".format(eventTime=eventTime,eventSummary=e.summary.value)  ## Unsere Aufruf Variabel
                            response = {'nextAppointment': nextAppointmentValue}
                            self.speak_dialog('nextapp', data=response)
                        else:
                            self.speak_dialog('events_done')

        except:
            self.speak_dialog("no_event")

    #Erweiterung für alle Events am heutigen Tag
    @intent_file_handler('events_today.intent')
    def handle_today_events(self, message):
            try:
                if len(calendars) > 0:
                    calendar = calendars[0]
                    events = calendar.date_search(today,
                                                  datetime.combine(today,
                                                                   time(23, 59, 59, 59)))  # Events am heutigen Tag
                    if len(events) == 0:
                        print("No events today!")
                    else:
                        print("Total {num_events} events:".format(num_events=len(events)))
                        for event in events:
                            event.load()
                            e = event.instance.vevent
                            if e.dtstart.value.strftime("%H:%M") == "00:00":
                                #Ausgabe von ganztägigen Events
                                eventTime = e.dtstart.value.strftime("%D")
                                print(
                                    "{eventTime} {eventSummary}".format(eventTime=eventTime,
                                                                        eventSummary=e.summary.value))
                                dayEvent = "{eventTime} {eventSummary}".format(eventTime=eventTime,
                                                                                        eventSummary=e.summary.value)  ## Unsere Aufruf Variabel
                                response = {'allDayEvent': dayEvent}
                                self.speak_dialog('events_today', data=response)
                            else:
                                # This is a "normal" event
                                eventTime = e.dtstart.value.strftime("%H:%M")
                                print(
                                    "{eventTime} {eventSummary})".format(eventTime=eventTime,
                                                                         eventSummary=e.summary.value))
                                hourAppointment = "{eventTime} {eventSummary})".format(eventTime=eventTime,
                                                                                             eventSummary=e.summary.value)
                                response = {'appointmentHour': hourAppointment}
                                self.speak_dialog('hourAppointment', data=response)
            except:
                self.speak_dialog("no_event")

def create_skill():
    return Nextapp()