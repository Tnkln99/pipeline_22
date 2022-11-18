import sys
from manager import engine
import importlib


def get():
    """
    Returns Engine depending on the context.
    :return:
    """
    executed_app_pattern = sys.executable
    executed_app = executed_app_pattern
    print(executed_app)
    if executed_app.find("maya") != -1:
        from manager.engine.maya import maya_engine as ma

        importlib.reload(ma)
        return ma.MayaEngine()
    else:
        from manager.engine import base_engine as be
        return be.BaseEngine()
