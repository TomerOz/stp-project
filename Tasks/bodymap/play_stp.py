""" TO-CHANGE :) The play_stp module holds the various classes of graphical or event objects
that are used for play sound in the BodyMap:
- GraphicalScene: Background graphical objects - silhouettes and buttons.
- SensationsCluster
- Trial - a two-phase instructions and rating routine.
"""
from psychopy import visual, gui,event, sound
import sounddevice as sd
import ctypes
import os
import numpy as np
from psychopy.constants import PLAYING

path_tovana = './Tasks/bodymap'
##TO DELETE WHEN I'll run it from run_sample?
def window():
    user32 = ctypes.windll.user32
    screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    win = visual.window.Window(units='pix', fullscr=True, size=screen_size,color='black', monitor=0) # To draw our objects in
    #I defined the color to 'black' becasue the Gui change the window size to be smaller.
    return win

def instructions(win):
    str_inst_stp= path_tovana+"/input/graphics/instructions/Slide2.JPG"
    inst_stp = visual.ImageStim(win=win,image=str_inst_stp, units='pix')
    return inst_stp

def end_button(win):
    str_end_button = path_tovana+'/input/graphics/Buttons/end_instructions_button.png'
    end_button = visual.ImageStim(win=win,image=str_end_button, units='norm', pos= (-0.003125, -0.8305555555555556))
    return end_button

def background_stp(win):
    str_cross = path_tovana+"/input/graphics/instructions/Slide3.JPG"
    cross = visual.ImageStim(win=win,image=str_cross, units='pix')
    return cross

def play_stp(win, neuORneg, additional_info):
    str_ID = str(additional_info['participant_id'])
    # str_cond = str(additional_info['cond'])
    sound_path = path_tovana+"/input/Audio/"+str_ID+"/"+neuORneg

    dir_audio = sorted(os.listdir(sound_path),reverse=True)
    print(dir_audio)
    playlist = []
    # if neuORneg == 'neu':
    for index_str_audio in range(0, len(dir_audio)):
        # index_str_audio = 0 #only for yoga and psychopterapy.
        music = sound.Sound(sound_path + '/' + dir_audio[index_str_audio])
        playlist.append(music)
    cross = background_stp(win)
    for i in range(0, len(playlist)):
        playlist[i].play()
        while playlist[i].status == PLAYING:
            cross.draw()
            win.flip()
    # else:  # neg
    #     for index_str_audio in range(0, 20):  # only for debuging
    #         # index_str_audio = 0 #only for yoga and psychopterapy.
    #         music = sound.Sound(sound_path_neg + '/' + dir_audio_neg[index_str_audio])
    #         playlist.append(music)
    #     cross = background_stp(win)
    #     for i in range(0, len(playlist)):
    #         playlist[i].play()
    #         while playlist[i].status == PLAYING:
    #             cross.draw()
    #             win.flip()
    win.flip()

def stp(win,block,additional_info):
    # win = window()
    inst_stp = instructions(win)
    endButton = end_button(win)
    taskMouse = event.Mouse(visible=True, win=win)  # build a mouse Psychopy object.
    read_inst = True
    while read_inst:
        inst_stp.draw()
        endButton.draw()
        win.flip()
        if taskMouse.isPressedIn(endButton):
            read_inst= False
    play_stp(win, block,additional_info)
    # win.close()
# play_stp('neu')
# win = window()
# stp('neu')
