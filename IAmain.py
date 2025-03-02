import openai
import pyaudio
import wave
import os
from vosk import Model, KaldiRecognizer

# Configura la clau d'API de OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Configura el model de reconeixement de veu Vosk
model = Model("model")
recognizer = KaldiRecognizer(model, 16000)


# Configura el micròfon per enregistrar
def record_audio():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    frames = []

    while True:
        data = stream.read(1024)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            print(f"Text reconegut: {result}")
            stream.stop_stream()
            break
        frames.append(data)

    return result


# Funció per generar resposta de ChatGPT
def chatgpt_response(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",  # Pot variar segons el model que vulguis
        prompt=prompt,
        max_tokens=150
    )
    return response.choices[0].text.strip()


# Funció per generar veu a partir de text amb Piper
def speak_text(text):
    os.system(f"espeak '{text}'")


# Ciclo principal
while True:
    print("Escoltant...")
    result = record_audio()
    text = result['text']
    if text:
        print(f"Tu has dit: {text}")
        response = chatgpt_response(text)
        print(f"IA diu: {response}")
        speak_text(response)
