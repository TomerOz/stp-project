import os
import shutil


class OutputOrganizer(object):
    def __init__(self, menu):
        self.menu = menu
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
