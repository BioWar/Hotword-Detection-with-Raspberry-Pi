import tflite_runtime.interpreter as tflite
import numpy as np
from pydub import AudioSegment
from threading import Thread
from queue import Queue
from time import time
import librosa
import pyaudio
import random
import glob
import sys
import io
import os
from pydub.playback import play


#input_data = np.array(outputFrame, dtype=np.float32)
#input_data = input_data[..., np.newaxis]
#input_data = input_data.reshape((1, 28, 28, 1))
#interpreter.set_tensor(input_details[0]['index'], input_data)
#interpreter.invoke()
#output_data = interpreter.get_tensor(output_details[0]['index']
#result = np.argmax(output_data)

def load_tflite_model():
    global interpreter, input_details, output_details
    interpreter = tflite.Interpreter(model_path="../models/model-rnn-comrade-44100-mel.v4.tflite")
    interpreter.allocate_tensors()

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    input_shape = input_details[0]['shape']

def model_predict(data):
    global interpreter, input_details, output_details
    input_data = np.array(data, dtype=np.float32)
    interpreter.set_tensor(input_details[0]["index"], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]["index"])
    return output_data

def get_mel_spectogram(data):
    n_fft = 2048
    hop_length = 512
    n_mels = 128
    S = librosa.feature.melspectrogram(data, sr=sr, n_fft=n_fft, hop_length=hop_length, n_mels=n_mels)
    S_DB = librosa.power_to_db(S, ref=np.max)
    return S_DB

def detect_triggerword_spectrum(data):
    data = data.swapaxes(0, 1)
    data = np.expand_dims(data, axis=0)
    predictions = model_predict(data)
    return predictions.reshape(-1)

def has_new_triggerword(predictions, chunk_duration, feed_duration, threshold):
    predictions = predictions > threshold
    chunk_predictions_samples = int(len(predictions) * chunk_duration / feed_duration)
    chunk_predictions = predictions[ - chunk_predictions_samples: ]
    level = chunk_predictions[0]
    for pred in chunk_predictions:
        if pred > level:
            return True
        else:
            level = pred
    return False

def callback(in_data, frame_count, time_info, status):
    global run, timeout, data
    if time() > timeout:
        run = False
    data0 = np.frombuffer(in_data, dtype=np.float32)
    #sys.stdout.write('.')
    print('.', end='')
    data = np.append(data, data0)
    if len(data) > feed_samples:
        data = data[-feed_samples: ]
        q.put(data)
    return (in_data, pyaudio.paContinue)

def get_audio_input_stream(callback):
    stream = pyaudio.PyAudio().open(
            format=pyaudio.paFloat32,
            #format=pyaudio.paInt16,
            channels=1,
            rate=sr,
            input=True,
            frames_per_buffer=chunk_samples,
            stream_callback=callback
        )
    return stream

if __name__=="__main__":
    activation_sound = AudioSegment.from_wav("../activation_sound/activation.wav")
    print("[INFO] Loading TFLite model...")
    load_tflite_model()
    print("[INFO] Model is successfully loaded...")

    chunk_duration = 2
    sr = 44100
    chunk_samples = int(sr * chunk_duration)

    feed_duration = 10
    feed_samples = int(sr * feed_duration)

    q = Queue()
    run = True
    timeout = time() + 1 * 60

    data = np.zeros(chunk_samples, dtype=np.float32)

    stream = get_audio_input_stream(callback)
    stream.start_stream()

    print("[INFO] Starting stream...")
    try:
        while run:
            data = q.get()
            spectrum = get_mel_spectogram(data)
            preds = detect_triggerword_spectrum(spectrum)
            new_trigger = has_new_triggerword(preds, chunk_duration, feed_duration, threshold=0.1)
            if new_trigger:
                #sys.stdout.write('A')
                print('A', end='')
                play(activation_sound)
            else:
                print('.')
    except (KeyboardInterrupt, SystemExit):
        stream.stop_stream()
        stream.close()
        timeout = time()
        run = False

    stream.stop_stream()
    stream.close()
    print("[INFO] End of main.py.")
