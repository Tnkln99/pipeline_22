import os
import sys


class BaseEngine(object):

    def __init__(self):
        self.implementations = ['open']

    def open(self, file_name):
        os.system("start " + file_name)

    def __str__(self):
        return f"[{__class__.__name__}]"
