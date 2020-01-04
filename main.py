from pydub import AudioSegment
from pydub.playback import play
import os
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3

'''from pydub import AudioSegment

sound = AudioSegment.from_mp3("./sample.mp3")
sound.export("./sample.ogg", format="ogg")'''

#CONSTANTES
FRAMES_PADY = 30
FRAMES_PADX = 30


class CellPad:
    def __init__(self):
        pass
    busy = False
    file_name = "./sample.ogg"
    volume = 0.7
    paused = False
    played = False
    stopped = True
    loop = False

    def drawPad(self, master=None):
        pad = ttk.Frame(master, width=100, height=150, relief=GROOVE)
        pad.pack_propagate(0)
        pad.pack(side=LEFT, padx=10, pady=10)

        self.label_name = ttk.Label(pad, text=os.path.basename(self.file_name), relief=FLAT, font='Times 10 italic')
        self.label_name.pack(pady=2)

        self.playphoto = PhotoImage(file='icons/play-button.png')
        self.playbtn = Button(pad, image=self.playphoto, command=self.onPause)
        self.playbtn.pack()

        self.continuephoto = PhotoImage(file='icons/next.png')

        self.buttons = ttk.Frame(pad, padding='5 5')
        self.buttons.pack()

        self.stopphoto = PhotoImage(file='icons/stop16.png')
        self.stopbtn = ttk.Button(self.buttons, image=self.stopphoto, command=self.onStop)
        self.stopbtn.grid(row=0, column=0)

        self.pausephoto = PhotoImage(file='icons/pause.png')
        '''self.pausebtn = ttk.Button(self.buttons, image=self.pausephoto, command=None)
        self.pausebtn.grid(row=0, column=1)'''

        self.loopphoto = PhotoImage(file='icons/circular-arrow16.png')
        self.loopbtn = ttk.Checkbutton(self.buttons, image=self.loopphoto, style='Toolbutton', command=not self.loop)
        self.loopbtn.grid(row=0, column=2)

    def onPause(self):
        if self.stopped:
            self.played = True
            self.stopped = False
            self.paused = False
        else:
            self.paused = not self.paused
        #self.paused = not self.paused

        if self.played:
            if self.paused:
                self.playbtn.configure(image=self.continuephoto)
            else:
                self.playbtn.configure(image=self.pausephoto)
        else:
            self.playbtn.configure(image=self.playphoto)

    def onStop(self):
        self.stopped = not self.stopped
        self.playbtn.configure(image=self.playphoto)




root = Tk()
root.attributes("-fullscreen", True)

#create a statusbar
statusbar = ttk.Label(root, text="Welcome to Melody", relief=SUNKEN, anchor=W, font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)

# Create the menubar
menubar = Menu(root)
root.config(menu=menubar)


# Create the submenu

subMenu = Menu(menubar, tearoff=0)

songslist = []

# songslist - contains the full path + filename
# songsListbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename(multiple=True)
    [add_to_songslist(f) for f in filename_path]


def add_to_songslist(filename):
    filename = os.path.basename(filename)
    index = 0
    songsListbox.insert(index, filename)
    songslist.insert(index, filename_path)
    index += 1


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music player build using Python Tkinter by @attreyabhatt')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

mixer.init()

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (songslist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

# ---LEFT FRAME---

leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

songsListbox = Listbox(leftframe, width=30, height=30)
songsListbox.pack(pady=10)

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


def del_song():
    selected_song = songsListbox.curselection()
    selected_song = int(selected_song[0])
    songsListbox.delete(selected_song)
    songslist.pop(selected_song)


delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=RIGHT)


# ---RIGHT FRAME---
rightframe = Frame(root)
rightframe.pack(pady=30)

# TOP FRAME -> Pads for background musics
topframe = ttk.Frame(rightframe, relief=SUNKEN)
topframe.pack(pady=20)

musicpads = []

for i in range(8):
    pad = CellPad()
    musicpads.append(pad)
    musicpads[i].drawPad(topframe)

# MIDDLE FRAME -> Pads for background and environment songs
middleframe = ttk.Frame(rightframe, relief=SUNKEN)
middleframe.pack(pady=20)

environmentpads = []

for i in range(8):
    pad = CellPad()
    environmentpads.append(pad)
    environmentpads[i].drawPad(middleframe)

# BOTTOM FRAME -> Pads for effect songs
bottomframe = ttk.Frame(rightframe, relief=SUNKEN)
bottomframe.pack(pady=20, side=BOTTOM)

effectpads = []

for i in range(8):
    pad = CellPad()
    effectpads.append(pad)
    effectpads[i].drawPad(bottomframe)

root.mainloop()

