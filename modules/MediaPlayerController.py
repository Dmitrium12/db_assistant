import platform
import subprocess


class MediaPlayerController:
    def __init__(self):
        self.os_type = platform.system()

    def play_pause(self):
        if self.os_type == 'Windows':
            self._windows_play_pause()
        elif self.os_type == 'Linux':
            self._linux_control("play-pause")

    def stop(self):
        if self.os_type == 'Windows':
            self._windows_control("stop")
        elif self.os_type == 'Linux':
            self._linux_control("stop")

    def next_track(self):
        if self.os_type == 'Windows':
            self._windows_control("next")
        elif self.os_type == 'Linux':
            self._linux_control("next")

    def previous_track(self):
        if self.os_type == 'Windows':
            self._windows_control("previous")
        elif self.os_type == 'Linux':
            self._linux_control("previous")

    @staticmethod
    def _windows_play_pause():
        from pycaw.pycaw import AudioUtilities
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.AudioSessionControl:
                control = session.AudioSessionControl
                if control and control.State == 1:
                    control.Stop()
                else:
                    control.Play()

    @staticmethod
    def _windows_control(action):
        from pycaw.pycaw import AudioUtilities, IAudioSessionControl2
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and isinstance(session.ControlInterface, IAudioSessionControl2):
                if action == "stop":
                    session.SimpleAudioVolume.SetMute(1, None)
                elif action == "next" or action == "previous":
                    pass

    @staticmethod
    def _linux_control(command):
        try:
            subprocess.run(["playerctl", command], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Failed to {command}: {e}")
