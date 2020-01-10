import os
import pydub
from os.path import isdir, isfile, join, basename
from tkinter import filedialog
import tkinter

def convertMP3toOGG(songpath, path):
    soundname = basename(songpath)
    sound = pydub.AudioSegment.from_mp3(songpath)
    sound.export(join((path, soundname)), format="ogg")


def file_conversor():
    path = join(os.getcwd(), "converted_songs")
    try:
        if not isdir(path):
            os.mkdir(path)
    except OSError:
        tkinter.messagebox.showinfo('Error', 'Creation of directory %s failed' % path)
    filespath = filedialog.askopenfilename(multiple=True)

    try:
        [convertMP3toOGG(f, path) for f in filespath]
    except OSError:
        tkinter.messagebox.showinfo('Error', 'Conversion of file(s) failed!')
    else:
        tkinter.messagebox.showinfo('Successful', 'Conversion of file(s) done!')
