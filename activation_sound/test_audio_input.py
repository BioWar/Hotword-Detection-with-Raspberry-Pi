# Test of audio input with Python.
# If using format=pyaudio.paInt16 we can get good quality audio recording then everything is fine.
# If using format=pyaudio.paFloat32 we can record only white noise, it's pretty bad, because
# librosa uses only float format, and we will need librosa alot. Despite on bad quality of "float"
# recording, main.py still could be usable.

from pydub import AudioSegment
import pyaudio
import numpy as np
import os
import sys
import wave

def record():
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        #format=pyaudio.paFloat32,
        channels=1,
        rate=44100,
        input=True,
        input_device_index=1,
        frames_per_buffer=1024)
    print("[INFO] Record input audio for 5 seconds...")

    input_audio = stream.read(5 * 44100)
    input_audio = np.frombuffer(input_audio, dtype=np.int16) # dtype=np.float32

    print("[INFO] Recording complete.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    output_filename = "recording.wav"
    wav_file = wave.open(output_filename, 'wb')

    wav_file.setnchannels(1)
    wav_file.setsampwidth(2)
    wav_file.setframerate(44100)

    wav_file.writeframes(input_audio)
    wav_file.close()

    print(f"[INFO] File recorded and saved to {output_filename}.")


if __name__=="__main__":
    record()
