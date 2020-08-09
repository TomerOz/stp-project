"""A full demo of the BodyMap package.
"""

from psychopy import visual, event, core
import ctypes

import classes
from registration_menu import registration
from play_stp import stp
from emotions_ratings import emotion_rating

class ConsoleBodyMap(object):
    def __init__(self, menu, flow):
        self.flow = flow
        self.menu = menu

    def start_body_map_flow(self):
        user32 = ctypes.windll.user32
        screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


         # To draw our objects in
        win = visual.window.Window(units='pix', fullscr=True, size=screen_size,
                                   color='white', monitor=0)

        # ID, condition = registration()
        ID, condition = 2, 1
        # # The buttons, avatars, etc.
        gscn = classes.GraphicalScene(win=win)
        # # An object to hold the drawn sensations
        cluster1 = classes.SensationsCluster(win=win)
        cluster2 = classes.SensationsCluster(win=win)
        mouse = event.Mouse(win=win)

        while True:
            keys = event.getKeys()
            if keys:
                # q quits the experiment
                if keys[0] == 'q':
                    core.quit()

            # ###baseline
            # phase = 'baseline_or_practice'
            # bmt_baseline = classes.BodyMapTask(
            #     win=win, scene=gscn, cluster=cluster1, mouse=mouse,
            #     additional_info=additional_info
            #     )
            # bmt_baseline.run_task()

            #Neutral
            block = 'neu'
            additional_info = {'participant_id': ID, 'cond': condition, 'block': block} #Participant_number, cond=pre/post, phase = baseline/neutral/negative
            stp(win,block,additional_info)
            emotion_rating(win,block, additional_info)
            bmt_neutral = classes.BodyMapTask(
                win=win, scene=gscn, cluster=cluster1, mouse=mouse,
                additional_info=additional_info, block=block
            )

            bmt_neutral.run_task(block)
            # core.quit()

            #Negative
            block = 'neg'
            #stp(win,block)
            additional_info = {'participant_id': ID, 'cond': condition, 'block': block} #Participant_number, cond=pre/post, phase = baseline/neutral/negative
            bmt_negative = classes.BodyMapTask(
                win=win, scene=gscn, cluster=cluster2, mouse=mouse,
                additional_info=additional_info, block=block
                )
            #emotion_rating(win,block, additional_info)
            # bmt_negative.run_task(block)

            core.quit()
            self.flow.next()

