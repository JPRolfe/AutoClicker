import pyautogui
from tkinter import *

def takeBoundedScreenShot(self, x1, y1, x2, y2):
    im = pyautogui.screenshot(region=(x1, y1, x2, y2))
    #x = datetime.datetime.now()
    #fileName = x.strftime("%f")
    #im.save("snips/" + fileName + ".png")

def createScreenCanvas(self):
    self.master_screen.deiconify()
    self.master.withdraw()

    self.screenCanvas = Canvas(self.picture_frame, cursor="cross", bg="grey11")
    self.screenCanvas.pack(fill=BOTH, expand=YES)

    self.screenCanvas.bind("<ButtonPress-1>", self.on_button_press)
    self.screenCanvas.bind("<B1-Motion>", self.on_move_press)
    self.screenCanvas.bind("<ButtonRelease-1>", self.on_button_release)

    self.master_screen.attributes('-fullscreen', True)
    self.master_screen.attributes('-alpha', .3)
    self.master_screen.lift()
    self.master_screen.attributes("-topmost", True)

def on_button_release(self, event):
    #self.recPosition()
    global direction 
    if self.start_x <= self.curX and self.start_y <= self.curY:
        direction = "rd"
        print("right down")
        self.takeBoundedScreenShot(self.start_x, self.start_y, self.curX - self.start_x, self.curY - self.start_y)

    elif self.start_x >= self.curX and self.start_y <= self.curY:
        direction = "ld"
        print("left down")
        self.takeBoundedScreenShot(self.curX, self.start_y, self.start_x - self.curX, self.curY - self.start_y)

    elif self.start_x <= self.curX and self.start_y >= self.curY:
        direction = "ru"
        print("right up")
        self.takeBoundedScreenShot(self.start_x, self.curY, self.curX - self.start_x, self.start_y - self.curY)

    elif self.start_x >= self.curX and self.start_y >= self.curY:
        direction = "lu"
        print("left up")
        self.takeBoundedScreenShot(self.curX, self.curY, self.start_x - self.curX, self.start_y - self.curY)
    
    global e_x
    e_x = self.curX
    global e_y 
    e_y = self.curY
    print("Screenshot Chosen end {} {}".format(e_x, e_y))
    self.exitScreenshotMode()
    return event



def exitScreenshotMode(self):
    print("Screenshot mode exited")
    self.screenCanvas.destroy()
    self.master_screen.withdraw()
    self.master.deiconify()

def on_button_press(self, event):
    # save mouse drag start position
    self.start_x = self.screenCanvas.canvasx(event.x)
    self.start_y = self.screenCanvas.canvasy(event.y)
    global s_x
    s_x = self.start_x
    global s_y
    s_y = self.start_y
    print("Screenshot Chosen begin {} {}".format(s_x, s_y))
    self.rect = self.screenCanvas.create_rectangle(self.x, self.y, 1, 1, outline='red', width=3, fill="blue")

def on_move_press(self, event):
    self.curX, self.curY = (event.x, event.y)
    # expand rectangle as you drag the mouse
    self.screenCanvas.coords(self.rect, self.start_x, self.start_y, self.curX, self.curY)

def recPosition(self):
    print(self.start_x)
    print(self.start_y)
    print(self.curX)
    print(self.curY)    