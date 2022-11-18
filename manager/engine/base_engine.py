import os
from manager.core.fm.file_search import entity_to_path


class BaseEngine(object):

    def __init__(self):
        self.implementations = ['open']

    def open(self, file_data, project_name):
        file_name = entity_to_path(project_name, file_data)
        os.system("start " + file_name)

    def __str__(self):
        return f"[{__class__.__name__}]"
