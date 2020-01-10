from pydub import AudioSegment
from pydub.playback import play
import os
import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import filedialog
from pygame import mixer
import pygame
import threading
import pydub
from os.path import isdir, join, basename, splitext

'''sound = AudioSegment.from_mp3("./Aaron Smith - Dancin (feat Luvli) - Krono Remix.mp3")
sound.export("./sample2.ogg", format="ogg")'''

#CONSTANTES
FRAMES_PADY = 30
FRAMES_PADX = 30
CHANNELS = 10
SONGEND = pygame.constants.USEREVENT

class CellPad:
    def __init__(self):
        pass
    busy = False
    file_name = None
    channel = None
    sound = None
    volume = 0.7
    paused = False
    played = False
    stopped = True
    loop = False

    def drawPad(self, master=None):
        pad = ttk.Frame(master, width=115, height=160, relief=GROOVE)
        pad.pack_propagate(0)
        pad.grid_propagate(0)
        pad.pack(side=LEFT, padx=5, pady=10)

        self.topframe = Frame(pad, width=100, height=25, relief=FLAT)
        self.topframe.pack(side=TOP, pady=2)
        self.topframe.pack_propagate(0)

        self.labelframe = Frame(self.topframe, relief=FLAT, width=80, height=25)
        self.labelframe.pack(side=LEFT, pady=2)
        self.labelframe.pack_propagate(0)

        self.closeframe = Frame(self.topframe, relief=FLAT)
        self.closeframe.pack(side=RIGHT, pady=2)

        self.label_name = ttk.Label(self.labelframe, text=os.path.basename(self.file_name if self.busy else "..."), relief=FLAT, font='Times 10 italic')
        self.label_name.pack(pady=2, side=LEFT)

        '''self.closeframe = Frame(pad, relief=FLAT, width=20, height=160)
        self.closeframe.pack(side=RIGHT, pady=5)
        self.closeframe.pack_propagate(0)'''

        self.close = ttk.Button(self.closeframe, text="X", command=self.onClose, width=0)
        self.close.pack(side=RIGHT, anchor=W, fill=X)

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
        self.loopbtn = ttk.Checkbutton(self.buttons, image=self.loopphoto, style='Toolbutton', command=self.onLoop)
        self.loopbtn.grid(row=0, column=1)
        #self.loopImg = Label(self.buttons, image=self.loopphoto)

        #self.loopbtn["onvalue"] = True
        #self.loopbtn["offvalue"] = False
        #self.loopbtn["variable"] = self.loop

        self.sclBtns = ttk.Frame(pad, padding='5 5')
        self.sclBtns.pack()

        self.scale = ttk.Scale(self.sclBtns, from_=0, to=100, orient=HORIZONTAL, command=self.setVol)
        self.scale.set(70)  # implement the default value of self.scale when music player starts
        self.scale.pack()

    def onLoop(self):
        self.loop = not self.loop
        if self.loop:
            self.stopbtn["state"] = DISABLED
            self.close["state"] = DISABLED
            self.loopbtn.select()
        else:
            self.stopbtn["state"] = ACTIVE
            self.close["state"] = ACTIVE
            self.loopbtn.deselect()
        statusbar["text"] = self.loop

    def getChannel(self):
        for i in range(CHANNELS):
            if not mixer.Channel(i).get_busy():
                return i
            else:
                if i== CHANNELS-1:
                    tkinter.messagebox.showerror('Channels full', 'Number maximum of channels reached')
                    return None

    def onPause(self):
        statusbar["text"] = self.file_name
        if self.stopped:
            self.played = True
            self.stopped = False
            self.paused = False
            self.channel = mixer.Channel(self.getChannel())
            self.sound = mixer.Sound(self.file_name)
            self.channel.play(self.sound)
            playinglist.append(self)
        else:
            if self.paused:
                self.channel.unpause()
                self.paused = False
            else:
                self.channel.pause()
                self.paused = True

        if self.played:
            if self.paused:
                self.playbtn.configure(image=self.continuephoto)
            else:
                self.playbtn.configure(image=self.pausephoto)
        else:
            self.playbtn.configure(image=self.playphoto)

    def onStop(self):
        if not self.stopped:
            self.channel.stop()
            self.stopped = True
            self.playbtn.configure(image=self.playphoto)
        else:
            pass

    def setVol(self, val):
        self.volume = float(val) / 100
        self.channel.set_volume(self.volume)

    def onClose(self):
        if self.stopped:
            statusbar["text"] = "close"
            self.label_name["text"] = "..."
            self.file_name = None
            self.busy = False
        else:
            statusbar["text"] = "close"
            self.loopbtn.grid_forget()
            self.loop = False
            self.loopbtn.grid(row=0, column=1)
            self.channel.stop()
            self.file_name = None
            self.channel = None
            self.sound = None
            self.busy = False
            self.paused = False
            self.played = False
            self.stopped = True
            self.label_name["text"] = "..."
            self.playbtn.configure(image=self.playphoto)

'''class FancyListbox(tkinter.Listbox):

    def __init__(self, parent, mscSongs, evrSongs, efxSongs, *args, **kwargs):
        Listbox.__init__(self, parent, *args, **kwargs)

        self.mscsgs = mscSongs
        self.evrsgs = evrSongs
        self.efxsgs = efxSongs

        self.addmenu = Menu(self)

        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_cascade(label="Add", menu=self.addmenu)


        self.addmenu.add_command(label="to Music")
        self.addmenu.add_command(label="to Environment")
        self.addmenu.add_command(label="to Effect")

        self.bind("<Button-3>", self.popup) # Button-2 on Aqua

    def popup(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def toMusic(self):
        selection = Listbox.curselection(0)
        selection = int(selection[0])
        for p in self.mscsgs:
            if not p.busy:
                p.file_name = songslist[selection]
                p.labelname.config(text=p.file_name)
                statusbar.config(text=p.file_name)
        pass

    def toEnviro(self):
        pass

    def toEffect(self):
        pass'''

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

pygame.init()
mixer.init()
mixer.set_num_channels(CHANNELS)

playinglist = []

songslist = []

# songslist - contains the full path + filename
# songsListbox - contains just the filename
# Fullpath + filename is required to play the music inside play_music load function

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename(multiple=True)
    [add_to_songslist(f) for f in filename_path]


def add_to_songslist(filename):
    full_filename = filename
    filename = os.path.basename(full_filename)
    songsListbox.insert(END, filename)
    songslist.append(full_filename)


menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About Melody', 'This is a music player build using Python Tkinter by @attreyabhatt')


subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

def convertMP3toOGG(songpath, path):
    statusbar["text"] = "Converting " + songpath
    soundname = basename(songpath)
    sound = pydub.AudioSegment.from_mp3(songpath)
    sound.export(join(path, splitext(soundname)[0] + ".ogg"), format="ogg")


def file_conversor():
    path = join(os.getcwd(), "converted_songs")
    try:
        if not isdir(path):
            os.mkdir(path)
    except OSError:
        tkinter.messagebox.showinfo('Error', 'Creation of directory %s failed' % path)
    filespath = filedialog.askopenfilename(multiple=True, title="Files to converter")

    try:
        statusbar["text"] = "Converting files..."
        [convertMP3toOGG(f, path) for f in filespath]
    except OSError:
        tkinter.messagebox.showinfo('Error', 'Conversion of file(s) failed!')
    else:
        tkinter.messagebox.showinfo('Successful', 'Conversion of file(s) done!')

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Conversor", menu=subMenu)
subMenu.add_command(label="MP3 to OGG", command=file_conversor)

mixer.init()

# Root Window - StatusBar, LeftFrame, RightFrame
# LeftFrame - The listbox (songslist)
# RightFrame - TopFrame,MiddleFrame and the BottomFrame

musicpads = []
environmentpads = []
effectpads = []

def del_song():
    selected_song = songsListbox.curselection()
    selected_song = int(selected_song[0])
    songsListbox.delete(selected_song)
    songslist.pop(selected_song)

def toMusic():
    selected_song = songsListbox.curselection()
    selected_song = int(selected_song[0])
    idx = 0
    for p in musicpads:
        if not p.busy:
            p.file_name = songslist[selected_song]
            p.label_name["text"] = os.path.basename(p.file_name)
            p.busy = True
            statusbar["text"] = p.file_name
            break
        else:
            if idx == len(musicpads)-1:
                tkinter.messagebox.showerror('Pads full', 'This audio pad is full, please delete a item to add another')
                break
        idx += 1

def toEnviro():
    selected_song = songsListbox.curselection()
    selected_song = int(selected_song[0])
    idx = 0
    for p in environmentpads:
        if not p.busy:
            p.file_name = songslist[selected_song]
            p.label_name["text"] = os.path.basename(p.file_name)
            p.busy = True
            statusbar["text"] = p.file_name
            break
        else:
            if idx == len(environmentpads) - 1:
                tkinter.messagebox.showerror('Pads full', 'This audio pad is full, please delete a item to add another')
                break
        idx += 1

def toEffect():
    selected_song = songsListbox.curselection()
    selected_song = int(selected_song[0])
    idx = 0
    for p in effectpads:
        if not p.busy:
            p.file_name = songslist[selected_song]
            p.label_name["text"] = os.path.basename(p.file_name)
            p.busy = True
            statusbar["text"] = p.file_name
            break
        else:
            if idx == len(effectpads) - 1:
                tkinter.messagebox.showerror('Pads full', 'This audio pad is full, please delete a item to add another')
                break
        idx += 1

def busyMonitory():
    while True:
        for cell in playinglist:
            if not cell.channel.get_busy():
                if cell.loop:
                    cell.channel.play(cell.sound)
                else:
                    cell.stopped = True
                    cell.playbtn.configure(image=cell.playphoto)
                    playinglist.remove(cell)

        #statusbar["text"] = len(playinglist)

# ---LEFT FRAME---
leftframe = Frame(root)
leftframe.pack(side=LEFT, padx=30, pady=30)

addButtons = Frame(leftframe)
addButtons.pack(side=TOP)

addMscBtn = ttk.Button(addButtons, text="+ Musics", command=toMusic)
addMscBtn.pack(side=LEFT)

addEvrBtn = ttk.Button(addButtons, text="+ Environments", command=toEnviro)
addEvrBtn.pack(side=LEFT)

addEfxBtn = ttk.Button(addButtons, text="+ Efects", command=toEffect)
addEfxBtn.pack(side=LEFT)

songsListbox = Listbox(leftframe, width=30, height=30)
songsListbox.pack(pady=10)

addBtn = ttk.Button(leftframe, text="+ Add", command=browse_file)
addBtn.pack(side=LEFT)


delBtn = ttk.Button(leftframe, text="- Del", command=del_song)
delBtn.pack(side=RIGHT)


# ---RIGHT FRAME---
rightframe = Frame(root)
rightframe.pack(pady=10)

# TOP FRAME -> Pads for background musics
topframe = ttk.Frame(rightframe, relief=SUNKEN)
topframe.pack(pady=5)

musiclabel = Label(topframe, relief=FLAT, text="Music Pads")
musiclabel.pack(pady=5)



for i in range(8):
    pad = CellPad()
    musicpads.append(pad)
    musicpads[i].drawPad(topframe)

# MIDDLE FRAME -> Pads for background and environment songs
middleframe = ttk.Frame(rightframe, relief=SUNKEN)
middleframe.pack(pady=5)

environmentlabel = Label(middleframe, relief=FLAT, text="Environment Pads")
environmentlabel.pack(pady=5)


for i in range(8):
    pad = CellPad()
    environmentpads.append(pad)
    environmentpads[i].drawPad(middleframe)

# BOTTOM FRAME -> Pads for effect songs
bottomframe = ttk.Frame(rightframe, relief=SUNKEN)
bottomframe.pack(pady=5)

effectlabel = Label(bottomframe, relief=FLAT, text="Effect Pads")
effectlabel.pack(pady=5)


for i in range(8):
    pad = CellPad()
    effectpads.append(pad)
    effectpads[i].drawPad(bottomframe)

t1 = threading.Thread(target=busyMonitory)
t1.start()

root.mainloop()

