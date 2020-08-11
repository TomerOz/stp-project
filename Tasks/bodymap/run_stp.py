from play_stp import stp
from psychopy import visual
import ctypes
from emotions_ratings import emotion_rating

user32 = ctypes.windll.user32
screen_size = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

win = visual.window.Window(units='pix', fullscr=True, size=screen_size,
                           color='white', monitor=0)
def main(): #function that I want to run only
    phase = 'neu'
    stp(win, phase)
    # emotion_rating(phase)
if __name__ == '__main__':
    main()