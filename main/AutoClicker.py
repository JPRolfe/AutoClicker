import GUI 

if __name__  == '__main__':
    listener = 1
    root = GUI.Tk()
    app = GUI.Application(root, listener)
    #listener = testingmain.keyboard.Listener(on_press=testingmain.on_press_outer)
    #listener.start()
    #processes = []
    #root.protocol("WM_DELETE_WINDOW", testingmain.on_closing)
    root.mainloop()