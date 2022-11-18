import maya.cmds as cmds

from manager.core.fm.file_search import entity_to_path
from manager.engine.base_engine import BaseEngine


class MayaEngine(BaseEngine):
    def __init__(self):
        super().__init__()
        self.implementations.append('reference')
        self.implementations.append('publish')

    def open(self, file_data):
        file_name = entity_to_path(file_data)
        cmds.file(file_name, o=True, force=True)

    def __str__(self):
        return f"[{__class__.__name__}]"


if __name__ == '__main__':
    print("ola")
