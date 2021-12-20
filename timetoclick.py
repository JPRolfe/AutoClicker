import time
from tkinter import BaseWidget
from pynput import mouse
from pynput.mouse import Listener

begin_time = None


def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    if pressed:
        global begin_time
        begin_time = time.time()
        #print(begin_time)
    else:
        print(time.time() - begin_time)
        #return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0}'.format(
        (x, y)))
    return False

# Collect events until released
if __name__  == '__main__':
    listener = mouse.Listener(on_click=on_click, on_scroll=on_scroll)
    listener.start()
    listener.join()
