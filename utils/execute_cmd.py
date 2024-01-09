def execute_cmd(self, cmd: str):
    if cmd == 'thanks':
        self.play("thanks")
    elif cmd == 'stupid':
        self.play("stupid")
    elif cmd == 'off':
        self.play("off", True)
        self.porcupine.delete()
        exit(0)
