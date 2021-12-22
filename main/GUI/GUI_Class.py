from tkinter import *
from tkinter import messagebox
from tkinter import IntVar
import datetime
from multiprocessing import Process, Queue, Value
from pynput.keyboard import Key, Listener, KeyCode


running = False
globalKey = None
counterVariable = Value('i', 0)


class Application():

    def __init__(self, master, listener):
        self.listener = listener
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
        master.geometry('1100x580+1700+800')  # set new geometry
        master.title('Random Mouse Clicker')
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

        self.myButtonAssign = Button(self.labelframe_keybind, text="Assign", command=self.assignKey)
        self.myButtonAssign.grid(row=0, column=1, padx=2)

        self.myButtonClear = Button(self.labelframe_keybind, text="Clear", command=self.clearKey)
        self.myButtonClear.grid(row=0, column=2, padx=2)

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
        
        self.master_screen = Toplevel(master)
        self.master_screen.withdraw()
        self.master_screen.attributes("-transparent", "blue")
        self.picture_frame = Frame(self.master_screen, background = "blue")
        self.picture_frame.pack(fill=BOTH, expand=YES)
        master.bind_all("<1>", lambda event:event.widget.focus_set())
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
        self.master.wm_state("iconic")

    def enableRange(self):
        self.numberofclicks.config(state='disabled')
        return
    
    def enableFiniteRange(self):
        self.numberofclicks.config(state='normal')
        return

    from .GUI_Methods.GUI_Set_Keybind import assignKey, clearKey

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

    from .GUI_Methods.GUI_Set_Area import createScreenCanvas, takeBoundedScreenShot, on_button_release, exitScreenshotMode
    from .GUI_Methods.GUI_Set_Area import on_button_press, on_move_press, recPosition

    def exit_application(self):
        print("Application exit")
        #self.listener.stop()
        self.master.quit()
