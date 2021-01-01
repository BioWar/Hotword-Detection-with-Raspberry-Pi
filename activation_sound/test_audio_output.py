# Test of audio output with Python. Nothing special in here.

from pydub import AudioSegment
from pydub.playback import play
from time import sleep

activation_sound = AudioSegment.from_wav("activation.wav")

for _ in range(5):
    play(activation_sound)
    sleep(3)
