import requests
import yaml
from fuzzywuzzy import process

from data import config


class HomeAssistant:
    def __init__(self):
        self.url = "http://192.168.0.112:9999/api"
        self.token = config.HOME_ASSISTANT_TOKEN
        self.HA_CMD_LIST = yaml.safe_load(open('data/home_assistant_entities.yaml', encoding='utf8'))

    def get_info(self, state):
        response = requests.get(
            url=f"{self.url}/states",
            headers={
                "Authorization": "Bearer " + self.token
            }
        )
        for entity in response.json():
            if entity["entity_id"] == state:
                return entity
        return response

    def send_process(self, command="выключи телевизор"):
        response = requests.post(
            url=f"{self.url}/services/conversation/process",
            json={"text": command},
            headers={
                "Authorization": "Bearer " + self.token,
                "content-type": "application/json"
            },
        )
        if response.status_code == 200:
            return True
        return False

    def voice_to_name(self, voice: str) -> str:
        words = voice.lower().split()
        best_match = None
        highest_score = 0
        for word in words:
            result, score = process.extractOne(word, self.HA_CMD_LIST.keys())
            if score > highest_score:
                highest_score = score
                best_match = result
        return best_match

    def validate_info(self, name: str):
        answer = name
        entity_config = self.HA_CMD_LIST.get(name)
        if entity_config:
            # Создание словаря, разделяя каждый элемент конфигурации на ключ и значение
            entity_details = {item.split(':')[0]: item.split(':')[1] for item in entity_config}
            entity_id = entity_details.pop("entity_id", None)
            if entity_id:
                responses = self.get_info(entity_id)
                for attribute_path, label in entity_details.items():
                    response = responses
                    try:
                        for attribute in attribute_path.split("."):
                            response = response[attribute]
                        answer += f" {label} {response}"
                    except KeyError:
                        continue
        return answer
