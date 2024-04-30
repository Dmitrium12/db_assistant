import json
import os
import struct
import time

import noisereduce as nr
import numpy as np
import pvporcupine
import vosk
import yaml
from fuzzywuzzy import fuzz
from pvrecorder import PvRecorder

import config
from utils import execute_cmd, play


class Jarvis:
    def __init__(self):
        self.recorder = None
        self.CDIR = os.getcwd()
        self.VA_CMD_LIST = yaml.safe_load(open('commands.yaml', encoding='utf8'))
        self.porcupine = pvporcupine.create(
            access_key=config.PICOVOICE_TOKEN,
            keywords=['jarvis'],
            sensitivities=[1]
        )
        self.kaldi_rec = vosk.KaldiRecognizer(vosk.Model("model_large"), 16000)

    def main(self):
        self.recorder = PvRecorder(
            device_index=config.MICROPHONE_INDEX,
            frame_length=self.porcupine.frame_length
        )
        self.recorder.start()
        self.play("run")
        time.sleep(0.5)
        ltc = time.time() - 1000
        while True:
            try:
                pcm = self.recorder.read()
                reduced_audio = nr.reduce_noise(
                    y=pcm,
                    sr=16000,
                    prop_decrease=0.6
                )
                if self.porcupine.process(reduced_audio) >= 0:
                    self.recorder.stop()
                    self.play("greet", True)
                    self.recorder.start()
                    ltc = time.time()
                while time.time() - ltc <= 10:
                    pcm = self.recorder.read()
                    sp = struct.pack("h" * len(pcm), *pcm)
                    if self.kaldi_rec.AcceptWaveform(sp):
                        if self.va_respond(json.loads(self.kaldi_rec.Result())["text"]):
                            ltc = time.time()
                        break
            except Exception as err:
                print(f"Unexpected {err=}, {type(err)=}")
                raise

    def va_respond(self, voice: str):
        print(f"Распознано: {voice}")
        for x in config.VA_ALIAS + config.VA_TBR:
            voice = voice.replace(x, "").strip()
        rc = {'cmd': '', 'percent': 0}
        for c, v in self.VA_CMD_LIST.items():
            for x in v:
                vrt = fuzz.partial_ratio(voice.lower(), x.lower())
                if vrt > rc['percent']:
                    rc['cmd'] = c
                    rc['percent'] = vrt
        if len(rc['cmd'].strip()) <= 0:
            return False
        elif rc['percent'] < 70 or rc['cmd'] not in self.VA_CMD_LIST.keys():
            self.play("not_found")
            time.sleep(1)
            return False
        else:
            execute_cmd.execute_cmd(self, rc['cmd'])
            return True

    def play(self, phrase, wait_done=True):
        play.play(self, phrase, wait_done)
