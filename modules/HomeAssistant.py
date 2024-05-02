import requests

from data import config


class HomeAssistant:
    def __init__(self):
        self.url = "http://192.168.0.112:9999/api"
        self.token = config.HOME_ASSISTANT_TOKEN

    def get_info(self, state):
        response = requests.get(
            url=f"{self.url}/states",
            headers={
                "Authorization": "Bearer " + self.token
            }
        )
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
