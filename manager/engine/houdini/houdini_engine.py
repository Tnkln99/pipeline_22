from manager.engine.base_engine import BaseEngine
from manager.core.fm.file_search import entity_to_path

import hou


class HoudiniEngine(BaseEngine):
    def __init__(self):
        super().__init__()
        self.implementations.append('merge')

    def open(self, file_data):
        file_name = entity_to_path(file_data)
        hou.hipFile.load(file_name)
