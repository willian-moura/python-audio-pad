import os
import pydub
from os.path import isfile, join
mypaths = ["./spell.wav", "./swing.wav", "./sword-unsheathe4.wav"]
for f in os.listdir(mypath):
    if isfile(join(mypath, f)):
        sound = pydub.AudioSegment.from_wav(f)
        sound.export(f, format="ogg")