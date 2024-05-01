import random

import simpleaudio as sa


def play(self, phrase, wait_done=True):
    filename = None
    file_array = ["not_found", "thanks", "run", "stupid", "ready", "off"]
    if phrase == "greet":
        filename = f"greet{random.choice([1, 2, 3])}.wav"
    elif phrase == "ok":
        filename = f"ok{random.choice([1, 2, 3])}.wav"
    elif phrase in file_array:
        filename = f"{phrase}.wav"
    if wait_done:
        self.recorder.stop()
    if filename:
        wave_obj = sa.WaveObject.from_wave_file(f"{self.CDIR}/data/sound/{filename}")
        play_obj = wave_obj.play()
        if wait_done:
            play_obj.wait_done()
            self.recorder.start()
    else:
        print("tts")
