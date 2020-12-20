import mingus.core.notes as notes
import playsound
from random import randint
import threading
import asyncio
from time import sleep

############# namespace ############
class Model:
    PATH = 'c:/Users/joshn/OneDrive/Documents/C++ Projects/Music Sim/edited/{}.mp3'
    FIRST_NOTE = 'A'
    OFFSET = notes.note_to_int(FIRST_NOTE)
    NOTES_IN_OCTAVE = 12
    INIT_OCTAVE = 1
    UPPER_LIMIT = 88

    @staticmethod
    def note_to_int(note, octave=1):
        assert 0 <= octave <= 9
        off = notes.note_to_int(note) - Model.OFFSET
        # invert if C <= note < A, like a -ve congruence class
        off = Model.NOTES_IN_OCTAVE + off if off < 0 else off
        # 1-indexed
        return off + ((octave - Model.INIT_OCTAVE) * Model.NOTES_IN_OCTAVE) + 1

    @staticmethod
    def int_to_note(note):
        # revert the above
        assert 1 <= note <= Model.UPPER_LIMIT
        note = (((note - 1) % Model.NOTES_IN_OCTAVE) + Model.OFFSET) % Model.NOTES_IN_OCTAVE
        return notes.int_to_note(note)

    # Ex: play('A3'), play(12), play('C#', 2)
    # NOTE: play('A1', 2) will play A1
    @staticmethod
    def play(note, octave=1): 
        if type(note) == str:
            if note[-1].isdigit():
                note = Model.note_to_int(note[:-1], int(note[-1]))
            else:
                note = Model.note_to_int(note, octave)    

        assert 1 <= note <= Model.UPPER_LIMIT
        playsound.playsound(Model.PATH.format(note), True)

class Scheduler:
    def __init__(self):
        self.threads = []

    def schedule(self, work, arg_tuple):
        self.threads.append(
            threading.Thread(
                target=work, args=arg_tuple
            )
        )
    
    def start_all(self):
        for t in self.threads:
            t.start()

    def join(self, idx): 
        self.threads[idx].join()


########## Models a musical major/minor diatonic scale. ########
############## Goes from root -> root (+1 octave) ##############
class Scale:
    WS, HS = 2, 1
    MAJ_DELTAS = (WS, WS, HS, WS, WS, WS, HS)
    MIN_DELTAS = (WS, HS, WS, WS, HS, WS, WS)
    CHORDS = {
        'maj':,
        'min',
        '7th',
        'dim',
        'aug',
        'D7',
        'hD7'
    }

    def __init__(self, root, major, octave=3):
        self.root = root
        self.octave = octave

        root_off = Model.note_to_int(root, self.octave)
        self.notes = [root_off]
        deltas = Scale.MAJ_DELTAS if major else Scale.MIN_DELTAS
        for i in range(len(deltas)):
            self.notes.append(self.notes[i] + deltas[i])

    def set_octave(self, oct): self.octave = oct

    def play_chord(self, type: str):
        pass

    def _work(self, sec, idx):
        sleep(sec)
        # print('thread says hi', self.notes[idx])
        Model.play(self.notes[idx], self.octave)

    # plays a tonal song (starts + ends with the root of scale)
    def play_random_song(self, num_iters, speedup=1):
        sch = Scheduler()
        sch.schedule(self._work, (0, 0))
        sch.schedule(self._work, (num_iters/speedup, 0))

        for i in range(num_iters):
            idx = randint(0, len(self.notes)-1)
            sch.schedule(self._work, (i/speedup, idx))
            
        sch.start_all()
        sch.join(-1)
        

# demo
test = Scale('C', True)
test.set_octave(4)
test.play_random_song(100, speedup=2)