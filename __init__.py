from mycroft import MycroftSkill, intent_file_handler
import caldav
import os
from caldav.elements import dav
from datetime import datetime, timedelta, time, date
today  = datetime.combine(datetime.today(), time(0,0))
# Caldav url
# Die Credentials werden aus Sicherheitsgründen nicht direkt in der File abgelegt.
username =""
password =""
#username = os.environ.get('_siNextcloudUser')
#password = os.environ.get('_siNextcloudPW')

# Verbindungsaufbau zur Nextcloud der Veranstaltung SI20/21
url = "https://" + username + ":" + password + "@next.social-robot.info/nc/remote.php/dav"
# open connection to calendar
client = caldav.DAVClient(url)
principal = client.principal()
calendars = principal.calendars()

#Hier Beginnt der eigentliche Skill für MyCroft
class Nextapp(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
    #Intenthandler für die Abfrage des nächsten Termins am heutigen Tag.
    @intent_file_handler('nextapp.intent')
    def handle_nextapp(self, message):
        try:
            #Überprüfung des Kalenders ob Events am heutigen Tag eingetragen sind.
            if len(calendars) > 0:
                calendar = calendars[0]
                events = calendar.date_search(today,
                                              datetime.combine(today, time(23, 59, 59, 59)))  # Events am heutigen Tag
                #Falls keine Events vorhanden sind, soll die Ausgabe "Keine Events eingetragen" kommen.
                if len(events) == 0:
                    self.speak_dialog("no_event")
                else:
                    #Aufllistung der heutigen Events:
                    print("Total {num_events} events:".format(num_events=len(events)))
                    listNextAppointments = []
                    for event in events:
                        event.load()
                        e = event.instance.vevent
                        #Einlesen der Eventzeit
                        eventTime = e.dtstart.value.strftime("%H:%M")
                        eventVal = "{eventTime} {eventSummary}".format(eventTime=eventTime,
                                                                       eventSummary=e.summary.value)
                        #Überprüfung der aktuellen Zeit.
                        aktuelleZeit = datetime.now().strftime("%H:%M") #%H Stunden %M Minuten
                        #Falls der Termin nahc der aktuellen Uhrzeit ist wird er der Liste hinzugefügt.
                        if aktuelleZeit < eventTime:
                            listNextAppointments.append((eventVal))
                            print(listNextAppointments)
                        # Falls ein Tagesevent stattfindet soll dies auch dem Nutzer mitgeteilt werden.
                        elif e.dtstart.value.strftime("%H:%M") == "00:00": #00:00 Wird Als Startzeit von Tagesevents genutzt.
                            dailyEventSum = "{eventSummary}".format(eventSummary=e.summary.value)
                            response = {'dailyEventDialog':dailyEventSum}
                            self.speak_dialog('daily_event', data = response)
                        else:
                        #Falls kein weiterer Termin heute mehr vorhanden ist, soll demm Nutzer gesagt werden, dass
                        # alle Events schon durch sind.
                            self.speak_dialog('events_done')
                    listNextAppointments.sort()
                    # Rückgabewert an den Nutzer wird das nächste Event sein.
                    nextAppointmentValue = listNextAppointments[0]
                    response ={'nextAppointment':nextAppointmentValue}
                    #Die vordefinierte Antwort + das nächste Event werden von MyCroft an den Nutzer übergeben..
                    self.speak_dialog('nextapp', data=response)
        except:
            self.speak_dialog("no_event")

    #Aufruf alle Events am heutigen Tag zu erfahren
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
                print("Missing some Information. try to create a new event")
                #self.speak_dialog("no_event")
    #Bonusaufgabe Events am einem bestimmten Tag:
    @intent_file_handler('events_at.intent')
    def handle_events_at(self, message):
        #Abfrage des gesuchten Datums aus der verbalen Nutzer Anfrage / des Nutzerintents
        intentDatum = message.data.get('datum')
        print(intentDatum)
        try:
            #Bestimmen des gesuchten Datums
            #Formatierung des Datums auf die Reihenfolge DD-MM-YYYY
            setDatum = datetime.strptime(intentDatum, "%d-%m-%Y")
            endTime = datetime.combine(setDatum, time(23, 59, 59, 59))
            if len(calendars) > 0:
                calendar = calendars[0]
                #Direktes Datumsabruf
                events = calendar.date_search(start=setDatum,
                                      end=endTime)
                if len(events) == 0:
                    self.speak_dialog('no event')
                #Gleicher Codeaufruf wie bei den vorherigen Abfragen.
                else:
                    for event in events:
                        event.load()
                        e = event.instance.vevent
                        if e.dtstart.value.strftime("%H:%M") == "00:00":
                            # Ausgabe von ganztägigen Events
                            eventTime = e.dtstart.value.strftime("%D")
                            print(
                                "{eventTime} {eventSummary}".format(eventTime=eventTime,
                                                                    eventSummary=e.summary.value))
                            dayEvent = "{eventTime} {eventSummary}".format(eventTime=eventTime,
                                                                           eventSummary=e.summary.value)  ## Unsere Aufruf Variabel
                            response = {'allDayEvent': dayEvent}
                            self.speak_dialog('events_today', data=response)
                        else:
                            # Ausgabe von zeitlichen Events
                            eventTime = e.dtstart.value.strftime("%H:%M")
                            print(
                                "{eventTime} {eventSummary})".format(eventTime=eventTime,
                                                                     eventSummary=e.summary.value))
                            hourAppointment = "{eventTime} {eventSummary})".format(eventTime=eventTime,
                                                                                   eventSummary=e.summary.value)
                            response = {'appointmentHour': hourAppointment}
                            self.speak_dialog('hourAppointment', data=response)
        except:
            self.speak_dialog('got_no_date')

def create_skill():
    return Nextapp()