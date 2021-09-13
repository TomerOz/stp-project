#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import ipdb

BACKGROUND = "black"
FOREGROUND = "white"

IMAGEPATH_DICHOTIC_PRACTICE_ONE = "IMAGEPATH_DICHOTIC_PRACTICE_ONE"
IMAGEPATH_DICHOTIC_PRACTICE_TWO = "IMAGEPATH_DICHOTIC_PRACTICE_TWO"
IMAGEPATH_DICHOTIC = "IMAGEPATH_DICHOTIC"
IMAGEPATH_DICHOTIC_END = "IMAGEPATH_DICHOTIC_END"
IMAGEPATH_DCT_PRACTICE_1 = "IMAGEPATH_DCT_PRACTICE_1"
IMAGEPATH_DCT_PRACTICE_2 = "IMAGEPATH_DCT_PRACTICE_2"
IMAGEPATH_DCT_PRACTICE_3 = "IMAGEPATH_DCT_PRACTICE_3"
IMAGEPATH_DICHOTIC_BREAK = "IMAGEPATH_DICHOTIC_BREAK"
IMAGEPATH_AFACT_INSTRUCTIONS = "IMAGEPATH_AFACT_INSTRUCTIONS"
IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE = "IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE"
IMAGEPATH_MAB_INSTRUCTIONS = "IMAGEPATH_MAB_INSTRUCTIONS"
IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC = "IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC"
IMAGEPATH_CONTROL_INSTRUCTIONS = "IMAGEPATH_CONTROL_INSTRUCTIONS"
IMAGEPATH_CONTROL_INSTRUCTIONS_AFTER_PRACTICE = "IMAGEPATH_CONTROL_INSTRUCTIONS_AFTER_PRACTICE"
IMAGEPATH_BMM_INSTRUCTIONS = "IMAGEPATH_BMM_INSTRUCTIONS"
IMAGEPATH_END_OF_EXPERIMENT = "IMAGEPATH_END_OF_EXPERIMENT"


class InstructionsPaths(object):
    def __init__(self):
        # Dichotic:
        self.IMAGEPATH_DICHOTIC_PRACTICE_ONE = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst1'
        self.IMAGEPATH_DICHOTIC_PRACTICE_TWO = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst2'
        self.IMAGEPATH_DICHOTIC = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst3'
        self.IMAGEPATH_DICHOTIC_BREAK = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst4'
        # DCT:
        self.IMAGEPATH_DCT_PRACTICE_1 = r'.\\Instructions_Pictures\\DCT\\digit1'
        self.IMAGEPATH_DCT_PRACTICE_2 = r'.\\Instructions_Pictures\\DCT\\digit2'
        self.IMAGEPATH_DCT_PRACTICE_3 = r'.\\Instructions_Pictures\\DCT\\digit3'
        # AFCAT:
        self.IMAGEPATH_AFACT_INSTRUCTIONS = r'.\\Instructions_Pictures\\AFACT\\AFACT_main_instructions'
        self.IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE = r'.\\Instructions_Pictures\\AFACT\\AFACT_after_practice_instructions'
        # MAB:
        self.IMAGEPATH_MAB_INSTRUCTIONS = r'.\\Instructions_Pictures\\MAB\\MAB_main_instructions'
        self.IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC = r'.\\Instructions_Pictures\\MAB\\MAB_after_practice_instructions'
        # Control:
        self.IMAGEPATH_CONTROL_INSTRUCTIONS = r'.\\Instructions_Pictures\\Control\\\Control_main_instructions'
        self.IMAGEPATH_CONTROL_INSTRUCTIONS_AFTER_PRACTICE = r'.\\Instructions_Pictures\\Control\\\Control_after_practice_instructions'
        # BMM:
        self.IMAGEPATH_BMM_INSTRUCTIONS = r'.\\Instructions_Pictures\\BMM_Instructions\\BMM_pre_recordings'
        
        # General:
        self.IMAGEPATH_DICHOTIC_END = r'.\\Instructions_Pictures\\Dichotic\\EndOfTask'
        self.IMAGEPATH_END_OF_EXPERIMENT = r'Instructions_Pictures\EndOfExperiment'
        
        self.phases_instructions = {
            IMAGEPATH_DICHOTIC_PRACTICE_ONE: self.IMAGEPATH_DICHOTIC_PRACTICE_ONE,
            IMAGEPATH_DICHOTIC_PRACTICE_TWO: self.IMAGEPATH_DICHOTIC_PRACTICE_TWO,
            IMAGEPATH_DICHOTIC: self.IMAGEPATH_DICHOTIC,
            IMAGEPATH_DICHOTIC_BREAK: self.IMAGEPATH_DICHOTIC_BREAK,
            IMAGEPATH_DCT_PRACTICE_1: self.IMAGEPATH_DCT_PRACTICE_1,
            IMAGEPATH_DCT_PRACTICE_2: self.IMAGEPATH_DCT_PRACTICE_2,
            IMAGEPATH_DCT_PRACTICE_3: self.IMAGEPATH_DCT_PRACTICE_3,
            IMAGEPATH_AFACT_INSTRUCTIONS: self.IMAGEPATH_AFACT_INSTRUCTIONS,
            IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE: self.IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE,
            IMAGEPATH_MAB_INSTRUCTIONS: self.IMAGEPATH_MAB_INSTRUCTIONS,
            IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC: self.IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC,
            IMAGEPATH_CONTROL_INSTRUCTIONS: self.IMAGEPATH_CONTROL_INSTRUCTIONS,
            IMAGEPATH_CONTROL_INSTRUCTIONS_AFTER_PRACTICE: self.IMAGEPATH_CONTROL_INSTRUCTIONS_AFTER_PRACTICE,
            IMAGEPATH_BMM_INSTRUCTIONS: self.IMAGEPATH_BMM_INSTRUCTIONS,
            IMAGEPATH_DICHOTIC_END: self.IMAGEPATH_DICHOTIC_END,
            IMAGEPATH_END_OF_EXPERIMENT: self.IMAGEPATH_END_OF_EXPERIMENT,
        }
        
    def change_gender(self, gender):
        if gender == "f":
            self.IMAGEPATH_DICHOTIC_PRACTICE_ONE = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst1'
            self.IMAGEPATH_DICHOTIC_PRACTICE_TWO = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst2'
            self.IMAGEPATH_DICHOTIC = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst3'
            self.IMAGEPATH_DICHOTIC_BREAK = r'.\\Instructions_Pictures\\Dichotic\\DichoticInst4'
            # DCT:
            self.IMAGEPATH_DCT_PRACTICE_1 = r'.\\Instructions_Pictures\\DCT\\Female\\digit1'
            self.IMAGEPATH_DCT_PRACTICE_2 = r'.\\Instructions_Pictures\\DCT\\Female\\digit2'
            self.IMAGEPATH_DCT_PRACTICE_3 = r'.\\Instructions_Pictures\\DCT\\Female\\digit3'
            # AFCAT:
            self.IMAGEPATH_AFACT_INSTRUCTIONS = r'.\\Instructions_Pictures\\AFACT\\\Female\\AFACT_main_instructions'
            self.IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE = r'.\\Instructions_Pictures\\AFACT\\\Female\\AFACT_after_practice_instructions'
            # MAB:
            self.IMAGEPATH_MAB_INSTRUCTIONS = r'.\\Instructions_Pictures\\MAB\\MAB_main_instructions'
            self.IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC = r'.\\Instructions_Pictures\\MAB\\MAB_after_practice_instructions'
            # Control:
            self.IMAGEPATH_CONTROL_INSTRUCTIONS = r'.\\Instructions_Pictures\\Control\\Female\\Control_main_instructions'
            self.IMAGEPATH_CONTROL_INSTRUCTIONS_AFTER_PRACTICE = r'.\\Instructions_Pictures\\Control\\Female\\Control_after_practice_instructions'
            # BMM
            self.IMAGEPATH_BMM_INSTRUCTIONS = r'.\\Instructions_Pictures\\BMM_Instructions\\Female\\BMM_pre_recordings'
        
        self.phases_instructions = {
            IMAGEPATH_DICHOTIC_PRACTICE_ONE: self.IMAGEPATH_DICHOTIC_PRACTICE_ONE,
            IMAGEPATH_DICHOTIC_PRACTICE_TWO: self.IMAGEPATH_DICHOTIC_PRACTICE_TWO,
            IMAGEPATH_DICHOTIC: self.IMAGEPATH_DICHOTIC,
            IMAGEPATH_DICHOTIC_BREAK: self.IMAGEPATH_DICHOTIC_BREAK,
            IMAGEPATH_DCT_PRACTICE_1: self.IMAGEPATH_DCT_PRACTICE_1,
            IMAGEPATH_DCT_PRACTICE_2: self.IMAGEPATH_DCT_PRACTICE_2,
            IMAGEPATH_DCT_PRACTICE_3: self.IMAGEPATH_DCT_PRACTICE_3,
            IMAGEPATH_AFACT_INSTRUCTIONS: self.IMAGEPATH_AFACT_INSTRUCTIONS,
            IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE: self.IMAGEPATH_AFACT_INSTRUCTIONS_AFTER_PRACTICE,
            IMAGEPATH_MAB_INSTRUCTIONS: self.IMAGEPATH_MAB_INSTRUCTIONS,
            IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC: self.IMAGEPATH_MAB_INSTRUCTIONS_AFTER_PRACTIC,
            IMAGEPATH_CONTROL_INSTRUCTIONS: self.IMAGEPATH_CONTROL_INSTRUCTIONS,
            IMAGEPATH_CONTROL_INSTRUCTIONS_AFTER_PRACTICE: self.IMAGEPATH_CONTROL_INSTRUCTIONS_AFTER_PRACTICE,
            IMAGEPATH_BMM_INSTRUCTIONS: self.IMAGEPATH_BMM_INSTRUCTIONS,
            IMAGEPATH_DICHOTIC_END: self.IMAGEPATH_DICHOTIC_END,
            IMAGEPATH_END_OF_EXPERIMENT: self.IMAGEPATH_END_OF_EXPERIMENT,
        }
            



class Instructions(object):
    def __init__(self, gui, exp, flow, imagepaths, phase_key, is_end_screen=False):
        self.current_pic = 0
        self.exp = exp
        self.gui = gui
        self.flow = flow
        self.imagepaths = imagepaths
        self.is_end_screen = is_end_screen
        self.phase_key = phase_key
        
    def start_instrunctions(self, break_time=None):
        self.define_instructions_path()
        # defining break time
        if break_time == None:
            self.break_time = 0
        else:
            self.break_time = break_time
            
        self.current_pic = 0 # for reset
        self.gui.bind("<space>", self.next_pic)
        self.gui.bind("<space>", self.next_pic)
        self.exp.create_frame("instructions_f", 
                full_screen=True,
                background_color=BACKGROUND)
                
        img_path = self.imagepath +'\\' + self.instruction_pics[self.current_pic]
        self.exp.craete_smart_image_label("instructions_l", "instructions_f", img_path)
        
        self.exp.display_frame("instructions_f", ["instructions_l"])
            
    def show_message(self, text):
        self.exp.LABELS_BY_FRAMES["instructions_f"]["instructions_l"].destroy() 
        self.exp.create_label("instructions_l", "instructions_f", label_text=text)
        self.exp.display_frame("instructions_f", ["instructions_l"])
    
    def get_task_continue_function(self, continue_function):
        self.continue_function = continue_function
        
    def destroy_frame_after_delay(self, gui_event=None):
        self.exp.LABELS_BY_FRAMES["instructions_f"]["instructions_l"].destroy() 
        self.gui.unbind("<space>")
        self.continue_function()

    def present_simple_picture_frame(self, delay_time=None, message_text=None):
        self.exp.create_frame("instructions_f", 
                full_screen=True,
                background_color=BACKGROUND)
                
        img_path = self.imagepath +'\\' + self.instruction_pics[self.current_pic]
        self.exp.craete_smart_image_label("instructions_l", "instructions_f", img_path)
        
        self.gui.after(0, lambda: self.exp.display_frame("instructions_f", ["instructions_l"]))
        self.gui.after(delay_time, lambda: self.show_message(message_text))
        self.gui.after(delay_time, lambda: self.gui.bind("<space>", self.destroy_frame_after_delay))
        
    def next_pic(self, eff):
        self.current_pic+=1
        if self.current_pic < len(self.instruction_pics):
            img_path = self.imagepath +'\\' + self.instruction_pics[self.current_pic]
            self.exp.LABELS_BY_FRAMES["instructions_f"]["instructions_l"].destroy()
            self.exp.craete_smart_image_label("instructions_l", "instructions_f", img_path)
            self.exp.display_frame("instructions_f", ["instructions_l"])
        else:
            self.gui.unbind("<space>")
            if self.break_time == 0 and not self.is_end_screen:
                self.exp.hide_frame("instructions_f")
                self.flow.next()
            elif not self.is_end_screen:
                self.gui.after(self.break_time, lambda: self.gui.bind("<space>", self.flow.next))
                self.gui.after(self.break_time, lambda: self.exp.hide_frame("instructions_f"))
                
    def define_instructions_path(self):
        self.imagepath = self.imagepaths.phases_instructions[self.phase_key]
        self.instruction_pics = os.listdir(self.imagepath)