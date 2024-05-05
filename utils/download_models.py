import os
import sys

from data import config


def install_vosk_model() -> None:
    """
    Функция устанавливает заданную в конфигурационном файле модели
    
    :return: 
    """
    try:
        open('data/model_small/README')
    except Exception as e:
        print(e)
        if sys.platform == "linux" or sys.platform == "linux2":
            os.system(
                f"wget https://alphacephei.com/vosk/models/{config.VOSK_MODEL_NAME}.zip"
            )
            os.system(f"unzip {config.VOSK_MODEL_NAME}.zip")
            os.system(f"mv {config.VOSK_MODEL_NAME} data/model_small")
            os.system(f"rm -rf {config.VOSK_MODEL_NAME}.zip")
        elif sys.platform == "darwin":
            os.system(
                f"curl https://alphacephei.com/vosk/models/{config.VOSK_MODEL_NAME}.zip"
            )
            os.system(f"unzip {config.VOSK_MODEL_NAME}.zip")
            os.system(f"mv {config.VOSK_MODEL_NAME} data/model_small")
            os.system(f"rm -rf {config.VOSK_MODEL_NAME}.zip")
        elif sys.platform == "win32":
            os.system(
                f"curl https://alphacephei.com/vosk/models/{config.VOSK_MODEL_NAME}.zip --output 1.zip"
            )
            os.system('powershell -command "Expand-Archive 1.zip ./"')
            os.system(f"rename {config.VOSK_MODEL_NAME} data/model_small")
            os.system("del /s /q 1.zip")
