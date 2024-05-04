def execute_cmd(self, cmd: str, recognized_phrase: str, voice: str):
    if cmd == 'thanks':
        self.play("thanks")
    elif cmd == 'stupid':
        self.play("stupid")
    elif cmd == 'off':
        self.play("off", True)
        self.porcupine.delete()
        exit(0)
    elif cmd == 'home_assistant_execute':
        self.home_assistant.send_process(recognized_phrase)
    elif cmd == 'home_assistant_get':
        entity_name = self.home_assistant.voice_to_name(voice)
        entity_info = self.home_assistant.validate_info(entity_name)
        print(entity_info)
