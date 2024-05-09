import platform
import subprocess


class MediaPlayerController:
    """
    Модуль для манипуляции музыкой
    """
    def __init__(self):
        self.os_type = platform.system()

    def play_pause(self) -> None:
        """
        Запуск/остановка музыки

        :return:
        """
        if self.os_type == 'Windows':
            self._windows_play_pause()
        elif self.os_type == 'Linux':
            self._linux_control("play-pause")

    def next_track(self) -> None:
        """
        Включает следующею композицию

        :return:
        """
        if self.os_type == 'Windows':
            self._windows_control("next")
        elif self.os_type == 'Linux':
            self._linux_control("next")

    def previous_track(self) -> None:
        """
        Включает предыдущею композицию

        :return:
        """
        if self.os_type == 'Windows':
            self._windows_control("previous")
        elif self.os_type == 'Linux':
            self._linux_control("previous")

    def _windows_play_pause(self) -> None:
        """
        Запуск/остановка музыки в windows

        :return:
        """
        import win32con
        self.key_press(win32con.VK_MEDIA_PLAY_PAUSE)

    def _windows_control(self, action: str) -> None:
        """
        Включает предыдущею или следующею композицию в windows

        :return:
        """
        import win32con
        if action == "next":
            self.key_press(win32con.VK_MEDIA_NEXT_TRACK)
        elif action == "previous":
            self.key_press(win32con.VK_MEDIA_PREV_TRACK)

    @staticmethod
    def key_press(key_code: str) -> None:
        """
        Симуляция нажатия и отпускания клавиши

        :param key_code: str - какую кнопку нажать
        :return:
        """
        import win32api
        import win32con
        win32api.keybd_event(key_code, 0, 0, 0)
        win32api.keybd_event(key_code, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def _linux_control(command: str) -> None:
        """
        Запускает команду для linux систем

        :param command: str - команда для запуска
        :return:
        """
        try:
            subprocess.run(["playerctl", command], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to {command}: {e}")
