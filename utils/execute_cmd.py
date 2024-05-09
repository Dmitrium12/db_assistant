from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from modules.Jarvis import Jarvis
else:
    Jarvis = None


def execute_cmd(self: Jarvis, cmd: str, recognized_phrase: str, voice: str) -> None:
    """
    Функция выполняет полученные команды

    :param self: modules.Jarvis - объект основного модуля
    :param cmd: str - команда которую функция должна выполнить
    :param recognized_phrase: str - распознанная фраза из списка фраз
    :param voice: str - распознанная фраза без проверки по списку
    :return:
    """
    if cmd == 'thanks':
        self.play("thanks")
    elif cmd == 'stupid':
        self.play("stupid")
    elif cmd == 'off':
        self.play("off", True)
        self.porcupine.delete()
        exit(0)
    elif cmd == 'music_on':
        self.media_player_controller.play_pause()
    elif cmd == 'music_off':
        self.media_player_controller.play_pause()
    elif cmd == 'music_next':
        self.media_player_controller.next_track()
    elif cmd == 'music_previous':
        self.media_player_controller.previous_track()
    elif cmd == 'home_assistant_execute':
        self.home_assistant.send_process(recognized_phrase)
    elif cmd == 'home_assistant_get':
        entity_name = self.home_assistant.voice_to_name(voice)
        entity_info = self.home_assistant.validate_info(entity_name)
        print(entity_info)
    elif cmd == 'weather':
        city = self.weather.validate_city(voice)
        city_info = self.weather.get_info(city)
        print(city_info)
