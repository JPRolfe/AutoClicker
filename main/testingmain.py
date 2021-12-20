from ctypes import string_at
from multiprocessing import RawArray, process
from tkinter import *
from tkinter import messagebox
from tkinter import IntVar
import time
import pyautogui
import win32api, win32con, win32gui
import datetime
import secrets
import keyboard
from pynput import keyboard
from pynput.keyboard import Key, Listener, KeyCode
from multiprocessing import Process, Queue, Value

# Collect events until released
s_x = None
s_y = None
e_x = None
e_y = None
millisecond_lower = None
millisecond_higher = None
running = False
direction = None
rawKey = None
finalKey = None
globalKey = None
finiteReset = Queue()
ClickCounter = Queue()
finiteReset.put(False)
beginningVariable = True
lastOption = None
counterVariable = Value('i', 0)
class Application():

    def __init__(self, master):
        self.master = master
        self.rect = None
        self.x = self.y = 0
        self.start_x = None
        self.start_y = None
        self.curX = None
        self.curY = None
        self.switch = False
        #root.configure(background = 'red')
        #root.attributes("-transparentcolor","red")

        #root.attributes("-transparent", "blue")
        root.geometry('900x480+1700+800')  # set new geometry
        root.title('Random Mouse Clicker')
        self.menu_frame = Frame(master)
        self.menu_frame.pack(expand=YES, fill=BOTH)
        self.menu_frame.columnconfigure((0,1), weight=0, pad=10)
        self.bottommainframe = Frame(master)
        self.bottommainframe.pack(side="bottom", expand=YES, fill=BOTH)

        self.topmainframe = Frame(master)
        self.topmainframe.pack(side="top", expand=YES, fill=BOTH)

        self.leftframe = Frame(self.topmainframe)
        self.leftframe.pack(side="left", expand=YES, fill=BOTH)

        self.rightframe = Frame(self.topmainframe)
        self.rightframe.pack(side="right", expand=YES, fill=BOTH)


        self.framebuttons = Frame(self.rightframe)
        self.framebuttons.pack(side="right", expand=YES, fill=BOTH)

        self.labelframe_area = LabelFrame(self.framebuttons, highlightthickness=0, text="Set Area", )
        self.labelframe_area.pack(side="top", padx=20, expand=True, fill=BOTH)

        self.labelframe_click = LabelFrame(self.leftframe, highlightthickness=0, text="Autoclick")
        self.labelframe_click.pack(padx=20, expand=YES, fill=BOTH)

        
        self.labelframe_keybind = LabelFrame(self.framebuttons, highlightthickness=0, text="Set Keybind")
        self.labelframe_keybind.pack(side="bottom", padx=20, pady=20, expand=YES, fill=BOTH)


        self.labelframe_delay = LabelFrame(self.leftframe, highlightthickness=0, text="Set Delay")
        self.labelframe_delay.pack(expand=YES, fill=BOTH, pady=20, padx=20)


        self.setupforsetup = Frame(self.bottommainframe)
        self.setupforsetup.pack(side="left", expand=YES, fill=BOTH)

        self.labelframe_setup = LabelFrame(self.setupforsetup, highlightthickness=0, text="Current Setup", )
        self.labelframe_setup.pack(padx=20,fill=BOTH)

        self.setupbox1 = Frame(self.labelframe_setup)
        self.setupbox1.pack(side="left")

        self.setupbox2 = Frame(self.labelframe_setup)
        self.setupbox2.pack(side="left", padx=3)

        self.setupbox3 = Frame(self.labelframe_setup)
        self.setupbox3.pack(side="left", padx=3, pady=10)

        self.keybindtext = StringVar()
        self.keybindtext.set("None")

        self.keybindDir = Label(self.setupbox1, textvariable=self.keybindtext, bg="white")
        self.keybindDir.pack(side="bottom", fill=X)

        self.keybindlabel = Label(self.setupbox1, text="Current Keybind Allocated", height=1)
        self.keybindlabel.pack(side="top")

        self.delaytext = StringVar()
        self.delaytext.set("None")

        self.delayDir = Label(self.setupbox2, textvariable=self.delaytext, bg="white")
        self.delayDir.pack(side="bottom", fill=X)

        self.delaylabel = Label(self.setupbox2, text="Current Delay Allocated", height=1)
        self.delaylabel.pack(side="top")

        self.clickrvar = IntVar()
        self.clickrvar.set(0)
        self.clickrtext = StringVar
         
        #self.clickrtext.set("None")
        #print(str(self.clickrtext.value))
        self.clickrDir = Label(self.setupbox3, text=str(self.clickrvar), bg="white")
        self.clickrDir.pack(side="bottom", fill=X)

        self.clickrlabel = Label(self.setupbox3, text="Clicks Remaining", height=1)
        self.clickrlabel.pack(side="top")

        self.frameMinButton = Frame(self.bottommainframe)
        self.frameMinButton.pack(side="right", fill=BOTH, expand=YES)
        self.minimizebutton = Button(self.frameMinButton, text = "Mimimize", command=self.minim, background='lightgrey')
        self.minimizebutton.pack(pady=10, fill=Y, expand=YES)

        self.snipButton = Button(self.labelframe_area, text="Set Click Area", command=self.createScreenCanvas)
        self.snipButton.pack(pady=20)


        self.labeltext1 = StringVar()
        self.labeltext1.set("Lower Limit Value")

        self.labelDir = Label(self.labelframe_click, textvariable=self.labeltext1, height=1)
        self.labelDir.grid(row=0,column=0)

        self.labeltext2 = StringVar()
        self.labeltext2.set("Upper Limit Value")

        self.labelDir = Label(self.labelframe_click, textvariable=self.labeltext2, height=2)
        self.labelDir.grid(row=1,column=0)

        self.rangetxtbelow = Entry(self.labelframe_click, width=10)
        self.rangetxtbelow.bind("<KeyRelease>", self.updateDelaySetup)
        self.rangetxtbelow.bind("<FocusOut>", self.checkDelayLower)
        #self.rangetxtbelow.pack(expand=YES)

        self.clicked = StringVar()
        self.clicked.set("Milliseconds")

        self.secondscale = OptionMenu(self.labelframe_click, self.clicked, "Seconds", "Milliseconds", command=self.updateDelaySetup)

        self.myButton = Button(self.labelframe_keybind, text="Assign", command=self.assignKey)
        self.myButton.grid(row=0, column=1, padx=2)

        self.myButton = Button(self.labelframe_keybind, text="Clear", command=self.clearKey)
        self.myButton.grid(row=0, column=2, padx=2)

        self.rangetextabove = Entry(self.labelframe_click, width=10)
        self.rangetextabove.bind("<KeyRelease>", self.updateDelaySetup)
        self.rangetextabove.bind("<FocusOut>", self.checkDelayUpper)
        #self.rangetextabove.pack(expand=YES)
        

        self.rangetextabove.grid(row=1, column=2)
        self.rangetxtbelow.grid(row=0, column=2)
        self.secondscale.grid(row=0, column=4)

        self.ClickDelayLabelFrame = LabelFrame(self.labelframe_delay, text="Click Option")
        self.ClickDelayLabelFrame.pack(padx=10, side="left", fill=X)

        self.option = StringVar()
        self.option2 = StringVar()
        self.endlessclicking = Radiobutton(self.ClickDelayLabelFrame, command=self.enableRange, text="Endless Clicking", value="endless", var=self.option)
        self.finiteclicking = Radiobutton(self.ClickDelayLabelFrame, command=self.enableFiniteRange, text= "Finite Clicking", value="finite", var=self.option)
        self.option.set('endless')

        self.numberofclicks = Entry(self.ClickDelayLabelFrame, width=10, state='disabled')
        self.numberofclicks.bind("<KeyRelease>", self.updateClickSetup)
        self.numberofclicks.grid(row=2, column=8, padx=15)


        self.PressReleaseLabel = LabelFrame(self.labelframe_delay, text="Press & Release Click Delay")
        self.PressReleaseLabel.pack(padx=10, side="left", fill=X)    
            
        self.PressReleaseDelayOn = Radiobutton(self.PressReleaseLabel, command=self.enableDelayOn, text="On", value="On", var=self.option2)
        self.PressReleaseDelayOff = Radiobutton(self.PressReleaseLabel, command=self.enableDelayOff, text= "Off", value="Off", var=self.option2)  
        self.option2.set('On')      

        self.clickReleaseDelay = Entry(self.PressReleaseLabel, width=10, state='disabled')
        self.clickReleaseDelay.bind("<KeyRelease>", self.updateClickDelaySetup)
        self.clickReleaseDelay.grid(row=2, column=8)

        self.PressReleaseDelayOn.grid(row = 2, column=1)
        self.PressReleaseDelayOff.grid(row=1, column=1)

        self.finiteclicking.grid(row = 2, column=6)
        self.endlessclicking.grid(row=1, column=6)

        self.keybindentry = Entry(self.labelframe_keybind, width=10)
        self.keybindentry.bind("<KeyRelease>", self.clicker)
        self.keybindentry.grid(row=0, column=0)
        

        self.keybindentry.insert(END, "None")
        
        self.master_screen = Toplevel(root)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)
        root.bind_all("<1>", lambda event:event.widget.focus_set())
        self.key = self.keybindentry.get()

    def enableDelayOn(self):
        pass
        return

    def enableDelayOff(self):
        pass
        return

    def updateClickDelaySetup(self, key):
        pass
        return

    def updateClickSetup(self, key):
        try:
            int(self.numberofclicks.get())
        except:
            messagebox.showerror("Non-Integer Type Error", "Please input a Positive Integer")
            return 0

        counterVariable.value = int(self.numberofclicks.get())
        #global testingInt
        #testingInt = int(self.numberofclicks.get())
        print(counterVariable.value)
        #self.clickrtext.set(counterVariable)
        return 1

    def checkDelayLower(self, key):
        if self.rangetxtbelow.get() != "":
            print(self.rangetxtbelow.get())
            try:
                int(self.rangetxtbelow.get())
            except:
                messagebox.showerror("Non-Integer Type Error", "Please input a Positive Integer")
                return
            if int(self.rangetxtbelow.get()) <= 0:
                messagebox.showerror("Negative/Zero Type Error", "Please input a Positive Integer")

    def checkDelayUpper(self, key):
        if self.rangetextabove.get() != "":
            if self.rangetxtbelow.get() != "":
                if self.rangetxtbelow.get() >= self.rangetextabove.get():
                    messagebox.showerror("Upper Equals Lower Error", "Please input an Integer greater than the Lower Limit Value")

    def updateDelaySetup(self, key):
        print(self.rangetextabove.get())
        tempVariable = "None"
        if self.clicked.get() == 'Milliseconds':
            tempVariable = "ms"
        else:
            tempVariable = "s"
        
        if self.rangetxtbelow.get() == "" and self.rangetextabove.get() == "":
            self.delaytext.set("? < x < ? {}".format(tempVariable))   

        elif self.rangetxtbelow.get() == "":
            self.delaytext.set("? < x < {} {}".format(self.rangetextabove.get(), tempVariable))        

        elif self.rangetextabove.get() == "":
            self.delaytext.set("{} < x < ? {}".format(self.rangetxtbelow.get(), tempVariable))

        else:
            self.delaytext.set("{} < x < {} {}".format(self.rangetxtbelow.get(), self.rangetextabove.get(), tempVariable))

    def minim(self):
        root.wm_state("iconic")

    def enableRange(self):
        self.numberofclicks.config(state='disabled')
        return
    
    def enableFiniteRange(self):
        self.numberofclicks.config(state='normal')
        return

    def assignKey(self):
        print(rawKey)
        global finalKey
        self.keybindtext.set(str(rawKey).replace("'", ""))
        finalKey = KeyCode(char=rawKey)
        

    def clearKey(self):
        global rawKey
        rawKey = None
        self.keybindentry.delete(0, END)
        self.keybindentry.insert(END, "None")  
        self.keybindtext.set("None")
        global finalKey
        finalKey = None


    def clicker(self, event):
            self.keybindentry.delete(0, END)
            self.keybindentry.insert(END, event.keysym)            
            global rawKey
            rawKey = globalKey
            #return str(event.keysym)

    def update_delay(self):
        try:
            global millisecond_lower
            millisecond_lower = int(self.rangetxtbelow.get())
            global millisecond_higher
            millisecond_higher = int(self.rangetextabove.get())
        except:
            #messagebox.showerror("Integer Error", "Please enter an Integer")
            return 0
        return 1
    
    def clicking(self):
        if running == False:
            return 0
        elif running == True:
            return 1

    def on_activate_h(self):
        print('<ctrl>+<alt>+h pressed')

    def takeBoundedScreenShot(self, x1, y1, x2, y2):
        im = pyautogui.screenshot(region=(x1, y1, x2, y2))
        x = datetime.datetime.now()
        fileName = x.strftime("%f")
        #im.save("snips/" + fileName + ".png")

    def createScreenCanvas(self):
        self.master_screen.deiconify()
        root.withdraw()

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
        root.deiconify()

    def exit_application(self):
        print("Application exit")
        listener.stop()
        root.quit()

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

def clickMouse(s_x, s_y, e_x, e_y, millisecond_higher, millisecond_lower, direction):
    #print("{}, {}, {}, {}, {}, {}".format(s_x, s_y, e_x, e_y, millisecond_higher, millisecond_lower))
    try:
        if direction == "rd":
            x_coord = int(s_x+secrets.randbelow(int(e_x) - int(s_x)))
            y_coord = int(s_y+secrets.randbelow(int(e_y) - int(s_y)))

        elif direction == "ru":
            x_coord = int(s_x+secrets.randbelow(int(e_x) - int(s_x)))
            y_coord = int(e_y+secrets.randbelow(int(s_y) - int(e_y)))
        
        elif direction == "ld":
            x_coord = int(e_x+secrets.randbelow(int(s_x) - int(e_x)))
            y_coord = int(s_y+secrets.randbelow(int(e_y) - int(s_y)))
            
        elif direction == "lu":
            x_coord = int(e_x+secrets.randbelow(int(s_x) - int(e_x)))
            y_coord = int(e_y+secrets.randbelow(int(s_y) - int(e_y)))

        else:
            messagebox.showerror("Fatal Error", "Report to Joey if this happens")
            return 0
    except:
        messagebox.showerror("None Error", "Select an Area to click from")
        messagebox.showerror("Log Box", "sx {} sy {} ex {} ey {}".format(s_x, s_y, e_x, e_y))
        return 0
    try:
        delay = millisecond_lower + secrets.randbelow(millisecond_higher - millisecond_lower)
    except:
        messagebox.showerror("Non-Integer Type Error", "Please input a proper Delay Time")
        return 0
    delay = delay*0.001
    win32api.SetCursorPos((x_coord,y_coord))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x_coord,y_coord,0,0)
    click_delay = (30 + int(secrets.randbelow(40))) * 0.001
    time.sleep(click_delay)
    print(click_delay)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x_coord,y_coord,0,0)

    time.sleep(delay)

def updateClickCounter():
    pass
    return

def on_press(key):
    global beginningVariable
    global running
    global globalKey
    global lastOption
    #global testingInt
    #testingInt = testingInt - 1
    globalKey = key
    print(app.option.get())
    print(finalKey)
    print("key {}".format(running))
    if KeyCode(char=key) == finalKey:
        if beginningVariable == True:
            if(app.option.get() == 'endless'):
                if app.clicking() == 0:
                    app.update_delay()
                    p = proc_start()
                    p.start()
                    processes.append(p)   
                    switch()
                    print(processes)
            
                elif app.clicking() == 1:
                    print(processes)
                    for p in processes:
                        proc_stop(p)
                        processes.remove(p)
                    print(processes)
                    switch()
                    x_temp, y_temp = win32api.GetCursorPos()
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x_temp, y_temp,0,0)
                    beginningVariable = False
                    finiteReset.get()

                lastOption = 'endless'
            
            else:
                if app.clicking() == 0:
                    app.update_delay()
                    p = proc_start()
                    p.start()
                    processes.append(p)   
                    switch()
                    print(processes)
                    finiteReset.get()
                
                beginningVariable = False

                lastOption = 'finite'


        else:
            if lastOption == 'endless':
                if app.option.get() == 'endless':
                    if app.clicking() == 0:
                        app.update_delay()
                        p = proc_start()
                        p.start()
                        processes.append(p)   
                        switch()
                        print(processes)

                    elif app.clicking() == 1:
                        print(processes)
                        for p in processes:
                            proc_stop(p)
                            processes.remove(p)
                        print(processes)
                        switch()
                        x_temp, y_temp = win32api.GetCursorPos()
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x_temp, y_temp,0,0)
                else:
                    if app.clicking() == 0:
                        app.update_delay()
                        p = proc_start()
                        p.start()
                        processes.append(p)   
                        switch()
                        print(processes)
                        if finiteReset.empty() != True:
                            finiteReset.get()

                    elif app.clicking() == 1:
                        print(processes)
                        for p in processes:
                            proc_stop(p)
                            processes.remove(p)
                        print(processes)
                        switch()
                        x_temp, y_temp = win32api.GetCursorPos()
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x_temp, y_temp,0,0)
                        
                    lastOption = 'finite'


            elif lastOption == 'finite':
                if app.option.get() == 'endless':
                    print("ending!")
                    if finiteReset.empty() != True:
                        if finiteReset.get() == True:
                            switch()
                            for p in processes:
                                proc_stop(p)
                                processes.remove(p)
                            
                    if app.clicking() == 0:
                        app.update_delay()
                        p = proc_start()
                        p.start()
                        processes.append(p)   
                        switch()
                        print(processes)
                        #finiteReset.get()

                    elif app.clicking() == 1:
                        print(processes)
                        for p in processes:
                            proc_stop(p)
                            processes.remove(p)
                        print(processes)
                        switch()
                        x_temp, y_temp = win32api.GetCursorPos()
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x_temp, y_temp,0,0)

                    lastOption = 'endless'
                
                else:
                    print("testing")
                    if finiteReset.empty() != True:
                        if finiteReset.get() == True:
                            switch()
                            for p in processes:
                                proc_stop(p)
                                processes.remove(p)
                            finiteReset.put(False)
                    print("testing2")
                    if app.clicking() == 0:
                        app.update_delay()
                        p = proc_start()
                        p.start()
                        processes.append(p)   
                        switch()
                        print(processes)
                        if finiteReset.empty() != True:
                            finiteReset.get()

                    elif app.clicking() == 1:
                        print(processes)
                        for p in processes:
                            proc_stop(p)
                            processes.remove(p)
                        print(processes)
                        switch()
                        x_temp, y_temp = win32api.GetCursorPos()
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x_temp, y_temp,0,0)
                    
                    lastOption = 'finite'


def on_closing():
    listener.stop()
    try:
        for p in processes:
            proc_stop(p)
    except:
        pass
    root.destroy()
    return

def switch():
    global running
    if running == False:
        running = True
    else:
        running = False

def work(s_x, s_y, e_x, e_y, millisecond_higher, millisecond_lower, direction, option, limit, finiteReset, counterVariable):
    global running
    if option == 'endless':
        finiteReset.put(False)
        print("hi!")
        while True:
            if clickMouse(s_x, s_y, e_x, e_y, millisecond_higher, millisecond_lower, direction) == 0:
                return 0

    elif option == 'finite':
        finiteReset.put(False)
        try:
            limit = int(limit)
        except:
            messagebox.showerror("Limit Integer Error", "Enter an integer in the limit box")
            finiteReset.get()
            finiteReset.put(True)
            return 0
        i = 0
        while i < limit:
            if clickMouse(s_x, s_y, e_x, e_y, millisecond_higher, millisecond_lower, direction) == 0:
                return 0
            counterVariable.value = counterVariable.value - 1
            print(counterVariable.value)
            i += 1
        finiteReset.get()
        finiteReset.put(True)
        

def proc_start():
    p_to_start = Process(target=work, args=(s_x, s_y, e_x, e_y, millisecond_higher, millisecond_lower, direction, app.option.get(), app.numberofclicks.get(), finiteReset, counterVariable))
    return p_to_start


def proc_stop(p_to_stop):
    p_to_stop.terminate()

if __name__  == '__main__':
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    processes = []
    root = Tk()
    app = Application(root)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.mainloop()
    
