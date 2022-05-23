import os
import shutil

class OutputOrganizer(object):
    def __init__(self, menu, flow, gui):
        self.menu = menu
        self.flow = flow
        self.gui = gui
    def organize_output(self):
        subject = str(self.menu.menu_data["subject"])
        source = r'Tasks\bodymap\output'
        destination = os.path.join(r'Data\Subject_' + subject, "bodymap")
        if not os.path.exists(destination):
            os.mkdir(destination)
            shutil.move(source, destination)
        else:
            print("Subject "+ subject + " already has folder named bodymap, check its content")
        os.makedirs(os.path.join(source, "actions"))
        os.makedirs(os.path.join(source, "cluster"))

        # Adding also the audio data file
        source = os.path.join(r'Subjects\subject ' + subject, "audio_data.xlsx")
        destination = os.path.join(r'Data\Subject_' + subject, "audio_data")
        if not os.path.exists(destination):
            os.mkdir(destination)
            shutil.copyfile(source, os.path.join(destination, "audio_data.xlsx"))
        else:
            print("Subject "+ subject + " already has folder of audio data")
        self.gui.after(100, self.flow.next)