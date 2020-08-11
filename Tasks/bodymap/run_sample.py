"""A full demo of the BodyMap package.
"""

from psychopy import visual, event, core
import ctypes

from Tasks.bodymap import classes
from Tasks.bodymap.play_stp import stp
from Tasks.bodymap.emotions_ratings import emotion_rating

class ConsoleBodyMap(object):
    def __init__(self, menu, flow, gui):
        self.flow = flow
        self.menu = menu
        self.gui = gui

    def start_body_map_flow(self):
        print("start")

        user32 = ctypes.windll.user32
        screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


         # To draw our objects in
        win = visual.window.Window(units='pix', fullscr=True, size=screen_size,
                                   color='white', monitor=0)

        # ID, condition = registration()
        # ID, condition = 1, 1
        ID = self.menu.menu_data['subject']
        condition = self.menu.menu_data['session']
        # # The buttons, avatars, etc.
        gscn = classes.GraphicalScene(win=win)
        # # An object to hold the drawn sensations
        cluster1 = classes.SensationsCluster(win=win)
        cluster2 = classes.SensationsCluster(win=win)
        mouse = event.Mouse(win=win)

        while_bool = True

        while while_bool:
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

            print("a")

            #Neutral
            block = 'neu'
            additional_info = {'participant_id': ID, 'cond': condition, 'block': block} #Participant_number, cond=pre/post, phase = baseline/neutral/negative
            stp(win,block,additional_info)
            emotion_rating(win,block, additional_info)
            bmt_neutral = classes.BodyMapTask(
                win=win, scene=gscn, cluster=cluster1, mouse=mouse,
                additional_info=additional_info, block=block
            )

            #print("b")

            bmt_neutral.run_task(block)
            # core.quit()

            #print("c")
            while_bool = False
        win.close()
        # core.quit()
        self.gui.after(100, self.flow.next)

        #print("d")

            #Negative
            # block = 'neg'
            #stp(win,block)
            #emotion_rating(win,block, additional_info)

            # additional_info = {'participant_id': ID, 'cond': condition, 'block': block} #Participant_number, cond=pre/post, phase = baseline/neutral/negative
            # bmt_negative = classes.BodyMapTask(
            #     win=win, scene=gscn, cluster=cluster2, mouse=mouse,
            #     additional_info=additional_info, block=block
            #     )
            #emotion_rating(win,block, additional_info)
            # bmt_negative.run_task(block)

            #core.quit()

            #
