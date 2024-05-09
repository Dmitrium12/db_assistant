import environs
import ast

env = environs.Env()
env.read_env()

VA_ALIAS = ast.literal_eval(env.str("VA_ALIAS"))
VOSK_MODEL_NAME = env.str("VOSK_MODEL_NAME")
MICROPHONE_INDEX = env.int("MICROPHONE_INDEX")
PICOVOICE_TOKEN = env.str("PICOVOICE_TOKEN")

# home assistant
HOME_ASSISTANT_URL = env.str("HOME_ASSISTANT_URL")
HOME_ASSISTANT_TOKEN = env.str("HOME_ASSISTANT_TOKEN")

# weather
WEATHER_DEFAULT_CITY = env.str("WEATHER_DEFAULT_CITY")
WEATHER_URL = env.str("WEATHER_URL")
