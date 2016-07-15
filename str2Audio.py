#!/usr/bin/python

def strToMidi(msg, fileName):
    from pyknon.genmidi import Midi
    from pyknon.music   import NoteSeq
    from pyknon.music   import Note
    notes = {
        '0' : Note(value=0, octave=5), # Do
        '1' : Note(value=2, octave=5), # Re
        '2' : Note(value=4, octave=5), # Mi
        '3' : Note(value=5, octave=5), # Fa
        '4' : Note(value=7, octave=5), # Sol
        '5' : Note(value=9, octave=5), # La
        '6' : Note(value=11, octave=5), # Si
        '7' : Note(value=0, octave=6),
        '8' : Note(value=2, octave=6),
        '9' : Note(value=4, octave=6),
        'a' : Note(value=5, octave=6),
        'b' : Note(value=7, octave=6),
        'c' : Note(value=9, octave=6),
        'd' : Note(value=11, octave=6),
        'e' : Note(value=0, octave=7),
        'f' : Note(value=2, octave=7)
    }
    msgHex = msg.encode('hex');
    sequence = NoteSeq('C1')
    before = ''
    for i in msgHex:
        if before == i:
            sequence.append(Note(value=4, octave=7))
        sequence.append(notes[i])
        before = i
    midi = Midi(1, tempo = 290)
    midi.seq_notes(sequence, track=0)
    midi.write(fileName)

if __name__ == '__main__':
    import sys
    import os

    if len(sys.argv) < 2:
        msg = input('Message: ')
    else:
        msg = sys.argv[1]

    if len(sys.argv) < 3:
        fileName = input('Output File (.midi/.wav): ')
    else:
        fileName = sys.argv[2]

    strToMidi(msg, fileName)
    os.system('timidity ' + fileName + '.midi -Ow --output-mono -o '+filename+'.wav');
