#!/usr/bin/env python
# -*- coding: utf-8 -*-
import tkinter as tk
import ipdb

BACKGROUND = "black"
FOREGROUND = "white"

gender =    'gender'
group =     'group'
subject =   'subject'
session = 'session'

class Menu(object):
    def __init__(self, exp, gui, flow, ap, audiopath, data_manager, instructions_paths, reduced_for_omer=False):
        self.exp = exp
        self.gui = gui
        self.flow = flow
        self.data_manager = data_manager
        self.instructions_paths = instructions_paths
        self.ap = ap
        self.audiopath = audiopath
        self.reduced_for_omer = reduced_for_omer
        self.menu_data = {}
        self.create_menu()

    def create_menu(self):
        self.exp.create_frame('menu_frame', full_screen=True, background_color=BACKGROUND)

        self.exp.create_label('menu_label_1', 'menu_frame', label_bg = BACKGROUND)
        self.exp.create_label('menu_label_2', 'menu_frame', label_bg = BACKGROUND)
        self.exp.create_label('menu_label_3', 'menu_frame', label_bg = BACKGROUND)
        self.exp.create_label('menu_label_4', 'menu_frame', label_bg = BACKGROUND)
        self.exp.create_label('Button_label', 'menu_frame', label_bg = BACKGROUND)


        self.exp.create_question('menu_frame', 'menu_label_1', gender, u'  מגדר ', default_value="m")
        self.exp.create_question('menu_frame', 'menu_label_2', group, u'  קבוצה', default_value=0)
        self.exp.create_question('menu_frame', 'menu_label_3', subject, u'  נבדק', default_value=500)
        self.exp.create_question('menu_frame', 'menu_label_4', session, u'  סשן', default_value=1)
        self.exp.create_button('menu_frame', 'Button_label', "Start", self.start_space_callback, button_name="Start Experiment")

        # Validating numeric input only:
        entry_session = type(self.exp).ALL_ENTRIES[session]
        entry_session.config(validate="key")
        entry_session['validatecommand'] = (entry_session.register(self.testVal), '%P', '%d')

        entry_subject = type(self.exp).ALL_ENTRIES[subject]
        entry_subject.config(validate="key")
        entry_subject['validatecommand'] = (entry_subject.register(self.testVal), '%P', '%d')

        dy = 30
        self.places = {
        'menu_label_1':(self.exp.cx, self.exp.cy-dy),
        'menu_label_2':(self.exp.cx, self.exp.cy),
        'menu_label_3':(self.exp.cx, self.exp.cy+dy),
        'menu_label_4':(self.exp.cx, self.exp.cy+(2*dy)),
        'Button_label':(self.exp.cx, self.exp.cy+(3.5*dy)),
        }

    def testVal(self, inStr, acttyp):
        if acttyp == '1':  # insert
            if not inStr.isdigit():
                return False
        return True


    def show(self):
        self.gui.unbind("<space>")
        if self.reduced_for_omer:
            self.exp.display_frame('menu_frame', ['menu_label_3', 'menu_label_4',"Button_label"], use_place = self.places)
        else:
            self.exp.display_frame('menu_frame', ['menu_label_1', 'menu_label_2', 'menu_label_3', 'menu_label_4',"Button_label"], use_place = self.places)
    def get_decoded_group(self, group_code):
        key = {
                "L12": "0",
                "G56": "1",
                "V27": "2",
                "K45": "0",
                "T21": "1",
                "Y87": "2",
                "E33": "0",
                "W90": "1",
                "S20": "2",
        }

        return key[group_code]


    def start_space_callback(self, event=None):
        type(self.exp).BUTTONS["Start Experiment"].config(state="disabled")
        type(self.exp).BUTTONS["Start Experiment"].destroy()
        self.menu_data[gender] = type(self.exp).ALL_ENTRIES[gender].get()
        self.menu_data[group] = self.get_decoded_group(type(self.exp).ALL_ENTRIES[group].get())
        self.menu_data[subject] = type(self.exp).ALL_ENTRIES[subject].get()
        self.menu_data[session] = type(self.exp).ALL_ENTRIES[session].get()

        self.updated_audio_path  = self.audiopath + '\\' + 'subject ' + str(self.menu_data[subject])
        self.ap.process_audio(self.updated_audio_path) # process this subject audio files
        self.data_manager.__late_init__(self)
        self.exp.hide_cursor()
        # choosing the group
        tasks = self.tasks_pre + self.intervention_tasks[int(self.menu_data[group])] + self.tasks_post
        self.flow.add_tasks(tasks)
        self.instructions_paths.change_gender(self.menu_data[gender])
        self.flow.next()

    def add_tasks_options(self, tasks_pre, intervention_tasks, tasks_post):
        self.tasks_pre = tasks_pre
        self.tasks_post = tasks_post
        self.intervention_tasks = intervention_tasks
