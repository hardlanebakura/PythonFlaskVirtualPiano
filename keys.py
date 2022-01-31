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

keyboard_notes = {'6': 'A2', 'e': 'A3', 'p': 'A4', 'j': 'A5', 'b': 'A6', '%': 'G#2', 'W': 'G#3', 'O': 'G#4', 'H': 'G#5', 'V': 'G#6', '7': 'B2', 'r': 'B3', 'a': 'B4', 'k': 'B5', 'n': 'B6', '^': 'A#2', 'E': 'A#3', 'P': 'A#4', 'J': 'A#5', 'B': 'A#6', '1': 'C2', '8': 'C3', 't':
'C4', 's': 'C5', 'l': 'C6', 'm': 'C7', '2': 'D2', '9': 'D3', 'y': 'D4', 'd': 'D5', 'z': 'D6', '!': 'C#2', '*': 'C#3', 'T': 'C#4', 'S': 'C#5', 'L': 'C#6', '3': 'E2', '0': 'E3', 'u': 'E4', 'f': 'E5', 'x': 'E6', '@': 'D#2', '(': 'D#3', 'Y': 'D#4', 'D': 'D#5', 'Z': 'D#6',
 '4': 'F2', 'q': 'F3', 'i': 'F4', 'g': 'F5', 'c': 'F6', '5': 'G2', 'w': 'G3', 'o': 'G4', 'h': 'G5', 'v': 'G6', '$': 'F#2', 'Q': 'F#3', 'I': 'F#4', 'G': 'F#5', 'C': 'F#6'}

keyboard_sounds = {'6': 'A2', 'e': 'A3', 'p': 'A4', 'j': 'A5', 'b': 'A6', '%': 'Ab2', 'W': 'Ab3', 'O': 'Ab4', 'H': 'Ab5', 'V': 'Ab6', '7': 'B2', 'r': 'B3', 'a': 'B4', 'k': 'B5', 'n': 'B6', '^': 'Bb2', 'E': 'Bb3', 'P': 'Bb4', 'J': 'Bb5', 'B': 'Bb6', '1': 'C2', '8': 'C3', 't':
'C4', 's': 'C5', 'l': 'C6', 'm': 'C7', '2': 'D2', '9': 'D3', 'y': 'D4', 'd': 'D5', 'z': 'D6', '!': 'Db2', '*': 'Db3', 'T': 'Db4', 'S': 'Db5', 'L': 'Db6', '3': 'E2', '0': 'E3', 'u': 'E4', 'f': 'E5', 'x': 'E6', '@': 'Eb2', '(': 'Eb3', 'Y': 'Eb4', 'D': 'Eb5', 'Z': 'Eb6',
 '4': 'F2', 'q': 'F3', 'i': 'F4', 'g': 'F5', 'c': 'F6', '5': 'G2', 'w': 'G3', 'o': 'G4', 'h': 'G5', 'v': 'G6', '$': 'Gb2', 'Q': 'Gb3', 'I': 'Gb4', 'G': 'Gb5', 'C': 'Gb6'}


logging.info(keyboard_sounds)