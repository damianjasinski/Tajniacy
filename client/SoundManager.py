from typing import Iterable
from PyQt5.QtMultimedia import QSound

class SoundManager:
    def __init__(self, sounds : Iterable[str]):
        self.sounds = dict()
        for sound in sounds:
            soundObject = QSound("resources/sfx/"+sound+".wav")
            self.sounds[sound] = soundObject
            
    def play_sound(self, sound : str):
        soundObject:QSound = self.sounds[sound]
        soundObject.play()

    def loop_sound(self, sound : str):
        soundObject:QSound = self.sounds[sound]
        soundObject.setLoops(-1)
        soundObject.play()