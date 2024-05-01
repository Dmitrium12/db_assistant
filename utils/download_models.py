import os
import sys

from data import config


def install_vosk_model():
    try:
        open('data/model_small/README')
    except Exception as e:
        print(e)
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system(f"wget https://alphacephei.com/vosk/models/{config.MODEL_NAME}.zip")
            os.system(f"unzip {config.MODEL_NAME}.zip")
            os.system(f"mv {config.MODEL_NAME} data/model_small")
            os.system(f"rm -rf {config.MODEL_NAME}.zip")
        elif sys.platform == "darwin":
            os.system(f"curl https://alphacephei.com/vosk/models/{config.MODEL_NAME}.zip")
            os.system(f"unzip {config.MODEL_NAME}.zip")
            os.system(f"mv {config.MODEL_NAME} data/model_small")
            os.system(f"rm -rf {config.MODEL_NAME}.zip")
        elif sys.platform == "win32":
            os.system(f"curl https://alphacephei.com/vosk/models/{config.MODEL_NAME}.zip --output 1.zip")
            os.system('powershell -command "Expand-Archive 1.zip ./"')
            os.system(f"rename {config.MODEL_NAME} data/model_small")
            os.system("del /s /q 1.zip")
