import os
import sys
import wave
import json
import pyaudio

from vosk import Model, KaldiRecognizer

# Load the model
model = Model("//Users/esteve/raspiPY/vosk-model-small-es-0.42")
rec = KaldiRecognizer(model, 16000)

# Initialize PyAudio
p = pyaudio.PyAudio()

# Open the microphone stream
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

# Recognize speech from the microphone
while True:
    data = stream.read(4000)
    if rec.AcceptWaveform(data):
        print(rec.Result())
    else:
        print(rec.PartialResult())