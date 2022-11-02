import cmds

from manager.engine.base_engine import BaseEngine


class MayaEngine(BaseEngine):
    def __init__(self):
        super().__init__()
        self.implementations.append('reference')
        self.implementations.append('publish')

    def open(self, file_name):
        cmds.file(file_name, new=False, o=True, open=1, buildLoadSettings=1)

    def __str__(self):
        return f"[{__class__.__name__}]"


if __name__ == '__main__':
    print("ola")
