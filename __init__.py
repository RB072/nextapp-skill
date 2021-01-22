from mycroft import MycroftSkill, intent_file_handler


class Nextapp(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('nextapp.intent')
    def handle_nextapp(self, message):
        self.speak_dialog('nextapp')


def create_skill():
    return Nextapp()

