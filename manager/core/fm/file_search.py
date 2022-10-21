from manager import conf
from pathlib import Path

from manager.conf import apps


def pattern_format_correcter(pattern):  # to change "C\blabla\bla\bal to C/blabla/bla/bla" (this is for windows I guess)
    pattern_list = []
    pattern_list[:0] = str(pattern)
    res = ""
    for i in range(len(pattern_list)):
        if pattern_list[i] == '\\':
            pattern_list[i] = '/'
        res = res + pattern_list[i]
    return res


def get_all_filtered(project_name, types=["*"], tasks=["*"], states=["*"], extensions=["*"]):
    project_path = Path(conf.project_path_pattern) / conf.projects.get(project_name)
    generators = []
    for type in types:
        for task in tasks:
            for state in states:
                for ext in extensions:
                    """if ext in apps.get("cache") and state == "":
                        pattern = conf.cache_pattern_path.format(type=type, task=task, ext=ext)
                    else:"""
                    pattern = conf.global_pattern_path.format(type=type, task=task, state=state, ext=ext)
                    found = Path(project_path).rglob(pattern)
                    generators.append(found)
    for g in generators:
        for f in g:
            yield f

