import sys

from manager import engine
import importlib
import os
import inspect
from pathlib import Path
from manager.engine import base_engine as be
from manager.engine.maya import maya_engine as ma


def get():
    importlib.reload(ma)
    """
    Returns Engine depending on the context.
    :return:
    """
    executed_app_pattern = sys.executable
    executed_app = executed_app_pattern
    print(executed_app)
    if executed_app.find("maya") != -1:
        return ma.MayaEngine()
    else:
        return be.BaseEngine()
