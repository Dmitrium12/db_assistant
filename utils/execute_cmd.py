def execute_cmd(self, cmd: str, recognized_phrase: str, voice: str):
    if cmd == 'thanks':
        self.play("thanks")
    elif cmd == 'stupid':
        self.play("stupid")
    elif cmd == 'off':
        self.play("off", True)
        self.porcupine.delete()
        exit(0)
    elif cmd == 'home_assistant':
        self.home_assistant.send_process(recognized_phrase)
