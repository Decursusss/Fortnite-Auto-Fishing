# main.py
import queue
import sounddevice as sd
import vosk
import json
import win32api
import win32con
import time
import threading

class VoiceController:
    def __init__(self):
        self.q = queue.Queue()
        self.model = vosk.Model("vosk-model-small-ru-0.22")
        self.grammar = '["отключить автоматическая рыбалка", "автоматическая рыбалка", "поймать", "голосовое управление", "закинуть", "отключить голосовое управление"]'
        self.commands = ["отключить автоматическая рыбалка", "автоматическая рыбалка", "поймать", "голосовое управление", "закинуть", "отключить голосовое управление"]

        self.voice_mode = False
        self.auto_fishing = False

        self.thread = threading.Thread(target=self._recognize_loop, daemon=True)

    def left_click(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.1)

    def _callback(self, indata, frames, time_, status):
        if status:
            print(status)
        self.q.put(bytes(indata))

    def start(self):
        print("🎤 Запуск голосового управления...")
        self.thread.start()

    def is_auto_fishing_enabled(self):
        return self.auto_fishing

    def _recognize_loop(self):
        with sd.RawInputStream(
            samplerate=16000,
            blocksize=548,
            dtype='int16',
            channels=1,
            callback=self._callback
        ):
            print("🎙 Готов к приёму команд...")
            rec = vosk.KaldiRecognizer(self.model, 16000, self.grammar)

            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "").lower()
                    if text:
                        print(f"🗣 Распознано: {text}")
                        for word in self.commands:
                            if word in text:
                                if word in ["поймать", "закинуть"]:
                                    self.left_click()
                                elif word == "голосовое управление":
                                    print("🗣 Включаю голосовое управление")
                                    self.voice_mode = True
                                elif word == "отключить голосовое управление":
                                    self.voice_mode = False
                                    print("🗣 Отключаю голосовое управление")
                                elif word == "автоматическая рыбалка":
                                    self.auto_fishing = True
                                    print("🗣 Включаю автоматическую рыбалку")
                                elif word == "отключить автоматическая рыбалка":
                                    self.auto_fishing = False
                                    print("🗣 Откючаю автоматическую рыбалку")
                                break
