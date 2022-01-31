from os import listdir
from os.path import isfile, join
from log_config import logging

files = [f for f in listdir("{}".format("") + "static/keys_mp3") if isfile(join("{}".format("") + "static/keys_mp3", f))]
#this file configures the keys

keys = {}
notes = [file.split(".")[0] for file in files]

d = {
    "A":"G",
    "B":"A",
    "D":"C",
    "E":"D",
    "G":"F"
}

kb = ["6", "e", "p", "j", "b", "%", "W", "O", "H", "V", "7", "r", "a", "k", "n", "^", "E", "P", "J", "B", "1", "8", "t", "s", "l", "m", "2", "9", "y", "d", "z", "!", "*", "T", "S", "L", "3", "0", "u",
"f", "x", "@", "(", "Y", "D", "Z", "4", "q", "i", "g", "c", "5", "w", "o", "h", "v", "$", "Q", "I", "G", "C"]

keyboard_notes = {}
keyboard_sounds = {}

for note in notes:

    #same octave
    if len(note) == 2:
        if note[1] != "0" and note[1] != "1" and note[1] != "7" and note[1] != "8":
            keys[note] = note
        elif note[0] == "C" and note[1] == "7":
            keys[note] = note
    #change octave
    else:
        octave = note[0]
        note_in_octave = note[2]
        virtual_piano_octave = d[octave]
        virtual_piano_note = virtual_piano_octave + "#" + note_in_octave
        if note_in_octave != "0" and note_in_octave != "1" and note_in_octave != "7" and note_in_octave != "8":
            keys[note] = virtual_piano_note

logging.info(keys)
virtual_piano_notes = list(keys.values())
logging.info(virtual_piano_notes)

mp3_notes = [note for note in keys]
logging.info(mp3_notes)
logging.info(virtual_piano_notes)
sounds_notes = dict(zip(virtual_piano_notes, mp3_notes))
logging.info(sounds_notes)
logging.info(keys)

c = 0
for key in kb:
    keyboard_notes[key] = virtual_piano_notes[c]
    keyboard_sounds[key] = sounds_notes[virtual_piano_notes[c]]
    c = c + 1

logging.info(keyboard_notes)
logging.info(keyboard_sounds)