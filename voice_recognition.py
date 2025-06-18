import sounddevice as sd
import queue
import json
import webbrowser

from vosk import Model, KaldiRecognizer

q = queue.Queue()

# Устройство ввода — можно задать индекс микрофона вручную
device = 1  # None — по умолчанию; или поставь нужный номер

samplerate = 16000  # Частота дискретизации
model_path = "vosk-model-small-ru-0.22"  # Путь к модели

model = Model(model_path)
rec = KaldiRecognizer(model, samplerate)

def callback(indata, frames, time, status):
    if status:
        print("Ошибка захвата:", status)
    print('Данные поступают')
    q.put(bytes(indata))

def recognize():
    print("Говорите...")
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                           dtype='int16', channels=1, callback=callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print("Вы сказали:", text)
                    return text

command = recognize()

if "открой сайт" in command:
    print("Открываю сайт...")
    webbrowser.open("https://google.com")
else:
    print("Команда не распознана.")