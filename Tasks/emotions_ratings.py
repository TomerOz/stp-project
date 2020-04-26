#!/usr/bin/env python
# -*- coding: utf-8 -*-
from psychopy import visual, event, gui, core
import ctypes
import os
import pandas as pd
 
PATH_TO_IMAGES ='./emotions_ratings' 
#@#@ read the comments about the function "find_30rect_responses_pos(win,background_image)"
def window():
    user32 = ctypes.windll.user32
    screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    win = visual.window.Window(units='norm', fullscr=True, size=screen_size,color='black', monitor=0) # To draw our objects in
    print(screen_size)
    return win

def background_emotions(win):
    path = PATH_TO_IMAGES+'/1.jpg'
    background_image = visual.ImageStim(win=win,image=path, units='norm')
    # background_image.autoDraw = True
    return background_image

def endButton(win):
    path = PATH_TO_IMAGES+'/finish_green.png'
    endButton_image = visual.ImageStim(win=win, image=path, units='norm', pos=[-0.9,-0.85], size=[0.2,0.3])
    # endButton_image.autoDraw = True
    return endButton_image

def build_rect(win,position):
    rect = visual.Rect(
        win=win,
        pos=position,
        units="norm",
        width=0.156,
        height=0.2,
        fillColor=None,
        lineColor=None,
        lineWidth=4)
    return rect

def find_30rect_responses_pos(win,background_image):
    '''TO USE ONLY -if I  need to find the locations again due to resolution problems in different screens or change with the background image.
    the function enables to find 30 (6 emotions/lines X 5 responses) rectangles center positions (x,y) on the background image.
    it gets the background image and then save each discrete mouse clicks.
     for building rect Psychopy object on each rect
     it returns list_pose with the poses (x,y) of 30 rects'''
    background_image.draw()
    win.flip()
    list_pose = []
    refresh_rate = 60.0 #60 flip per second
    default_time = 120 #sec, 2 minutes
    time_window = default_time * refresh_rate
    time_window = int(time_window)
    clock = core.Clock()
    mouse_down_detected = False #for detecting a new msue click, not by the frame rate.
    myMouse = event.Mouse(visible=True, win=win)
    # for frame in range(time_window):
    while clock.getTime() < default_time:
        if any(myMouse.getPressed()):  # Any button pressed, no matter which
            if not mouse_down_detected: #not False = True, check if it's a new click, not a cuntinues click which samples any frame.
                click_pose = tuple(myMouse.getPos()) #(X,Y)
                list_pose.append(click_pose)
                mouse_down_detected = True
        else:
            mouse_down_detected = False
    event.waitKeys()
    win.close()
    return list_pose
    # build_dic_rect(list_pose)

##this list was returned from 'find_30rect_responses_pos(win,background_image)' for specific background image.
#the locations are using Norm units (0-1, wile (0,0) is the center of the screen).
list_NormPos_rect = [(0.5484375, 0.6055555555555555), (0.2765625, 0.5972222222222222), (0.0, 0.6027777777777777), (-0.2703125, 0.6027777777777777), (-0.540625, 0.6083333333333333), (0.5453125, 0.33611111111111114), (0.2765625, 0.33611111111111114), (0.0, 0.33611111111111114), (-0.2703125, 0.3388888888888889), (-0.54375, 0.3388888888888889), (0.546875, 0.07222222222222222), (0.2703125, 0.06666666666666667), (0.0, 0.06944444444444445), (-0.26875, 0.06944444444444445), (-0.5453125, 0.06944444444444445), (0.546875, -0.20277777777777778), (0.2734375, -0.2), (0.0015625, -0.2), (-0.2671875, -0.20277777777777778), (-0.540625, -0.19444444444444445), (0.5484375, -0.46944444444444444), (0.271875, -0.4666666666666667), (0.0015625, -0.4638888888888889), (-0.2671875, -0.4666666666666667), (-0.5421875, -0.46944444444444444), (0.5484375, -0.7388888888888889), (0.2703125, -0.7361111111111112), (0.0015625, -0.7333333333333333), (-0.2734375, -0.7361111111111112), (-0.540625, -0.7361111111111112)]
def build_dic_rect(win, list_NormPos_rect):
    '''this function gets the list_NormPos_Rect and build a dictionaries inside dictionary,
      the outer dict contains the emotions list, and the inner dicts contains the response number as keys and the rect images (psychopy rect) of each response as values
      it uses the function build_rect'''
    dic_rect = {}
    keys = ['sadness','anger','interest','anxiety','shame','distress']
    for key in keys:
        dic_rect[key]={}
    k=0 #index for emotion key
    n=1 #new key for 5 poses for responses per emotion
    j=0 #line index (steps of 5)
    for i in range(len(list_NormPos_rect)):
        n += 1  # move to the next index for rect position
        if i<j+5: #if it still the same line/emotion (5 rect responses per emotion)
            if i==0:
                n=1
                rect = build_rect(win, list_NormPos_rect[i])
                dic_rect[keys[k]][n] = rect  # build the dic_rect
            else:
                rect = build_rect(win,list_NormPos_rect[i])
                dic_rect[keys[k]][n]= rect #build the dic_rect
        if i==j+5: #finish the line
            j += 5  # move to the next 5 responses in the next line
            k += 1  # move to the next emotion key
            n = 1  # equate to the first response/rect pose in the new line
            rect = build_rect(win, list_NormPos_rect[i])
            dic_rect[keys[k]][n] = rect  # build the dic_rect
    print(dic_rect)
    return dic_rect
#
def draw_dic_rect(dic_rect,background_image):
    '''iterates over the 30 rect in dic_rect and draw each of them on the screen'''
    background_image.draw()
    for emotion_key in dic_rect.keys():
        for k in dic_rect[emotion_key].keys():
            rect = dic_rect[emotion_key][k]
            rect.draw()

def find_emotion_key(dic_rect, val_rec):
    '''this function aims to find the keys from its value - to find the keys of a chosen rect
    the function draw_next_rect calls to this function'''
    for emotion_key in dic_rect.keys():
        for num_key in dic_rect[emotion_key].keys():
            if dic_rect[emotion_key][num_key]==val_rec:
                return emotion_key, num_key

def draw_next_rect(win,dic_rect,rect,dic_data,draw_rect_list,button,background_image):
    '''this function is activated by the function Rating, when a new press on a rect is detected.
    then it updated the new response:
     update dic_data with the new response number.
     change the LineColor of the chosen rect to be red.
     update draw_rect_list --> the list with rect objects that should be presented on the screen. add the new rect and remove the previous rect in the same line (if exist)
     '''
    emotion_key, num_key = find_emotion_key(dic_rect, rect)
    response = {emotion_key:num_key}
    if emotion_key in dic_data.keys():
         print('dic_data[emotion_key]', dic_data[emotion_key])
         draw_rect_list.remove(dic_rect[emotion_key][dic_data[emotion_key]])
    dic_data.update(response)
    rect.lineColor = 'red'
    background_image.draw()
    draw_rect_list.append(rect) #add the new chosen rect
    [r.draw() for r in draw_rect_list] #draw again each rect
    button.draw() #draw the end button
    win.flip()

def rating(win,dic_rect,background_image, PHASE):
    '''the main function which runs during the rating,
    gets the input from the participants (the mouse clicks), present his responses on the screen (as a change with the colorLine of the chosen rect to be red),
    save the output (data) as dictionary and at the end as CSV file (with the emotions names and ratings).
    it calls the function "draw_next_rect" in each click on a rect.
    it enables the participant to change his response during the rating.
    while there are 6 responses - the participant is able the press the end button and finish this stage'''
    button = endButton(win) #calls the function endButton which build an ImageStime of psychopy.
    button.draw() #draw the button on the screen "behine the curtains".
    win.flip() #present it on the screen.
    taskMouse = event.Mouse(visible=True, win=win) #build a mouse Psychopy object.
    dic_data = {} #dic for the data - emotion and rating as a number {'saddness:5,...}
    draw_rect_list = [] # the list of the presented rect - maximum 1 rect in a line (emotion), whic meand max 6 rects in this list.
    end_button = False #check if the end button was pressed
    while end_button == False: #while it was'nt pressed
        if taskMouse.isPressedIn(button)==1 and len(dic_data.keys())==6: #only if the participant press on the end buttone after 6 responses.
            end_button = True
        # elif taskMouse.isPressedIn(dic_rect["sadness"][1]):
        for emotion_key in dic_rect: #very fast iteration (60 frames per sec) which checks if there is a preess on one of the 30 rects.
            for num_key in dic_rect[emotion_key]: #1-5 rect responses for emotion
                rect = dic_rect[emotion_key][num_key]
                if taskMouse.isPressedIn(rect): #if there is a press - call the fraw_nect_rect function!
                    draw_next_rect(win,dic_rect,rect,dic_data,draw_rect_list,button,background_image)
    if (end_button == True): #?#not sure the next 3 lines are neccesary
        print(dic_data)
        win.close()
    df = pd.DataFrame(dic_data, index=[0]) #save the dic_data ad Padnas data frame.
    df.to_csv(PHASE+'_phase_emotion.csv', index=False) #write it into CSV file.


def emotion_rating(PHASE):
    '''run the main functions in the task.'''
    win = window()
    background_image = background_emotions(win)
    dic_rect = build_dic_rect(win, list_NormPos_rect)
    draw_dic_rect(dic_rect,background_image)
    rating(win, dic_rect,background_image,PHASE)

emotion_rating('DCT')

