
def assignKey(self):
    #print(rawKey)
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