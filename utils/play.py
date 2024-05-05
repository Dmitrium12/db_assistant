import random

import simpleaudio as sa


def play(self, phrase: str, wait_done: bool = True) -> None:
    """
    Функция для запуска голосовой команды

    :param self: modules.Jarvis - объект основного модуля
    :param phrase: str - фраза для запуска голосовой команды
    :param wait_done: bool - нужно-ли ждать окончания фразы
    :return:
    """
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
