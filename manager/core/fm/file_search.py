from manager import conf
from pathlib import Path


def pattern_format_correcter(pattern):  # to change "C\blabla\bla\bal to C/blabla/bla/bla" (this is for windows I guess)
    pattern_list = []
    pattern_list[:0] = str(pattern)
    res = ""
    for i in range(len(pattern_list)):
        if pattern_list[i] == '\\':
            pattern_list[i] = '/'
        res = res + pattern_list[i]
    return res


def get_all_filtered_assets(project_name, name="*", task="*", version="*", state="*", exts=["*"]):
    project_path = Path(conf.project_path_pattern) / conf.projects.get(project_name)
    generators = []
    for ext in exts:
        pattern = conf.assets_pattern_path.format(name=name, task=task, version=version, state=state, ext=ext)
        found = Path(project_path).rglob(pattern)
        generators.append(found)
    for g in generators:
        for f in g:
            yield f


def get_all_filtered_shots(project_name, seq="*", shot="*", name="*", version="*", state="*", exts=["*"]):
    project_path = Path(conf.project_path_pattern) / conf.projects.get(project_name)
    generators = []
    for ext in exts:
        pattern = conf.shots_pattern_path.format(name=name, state=state, ext=ext)
        found = Path(project_path).rglob(pattern)
        generators.append(found)

    for g in generators:
        for f in g:
            yield f


if __name__ == '__main__':
    states = ["__work", "__publish"]
    extensions = ['ma', 'mb', 'hipnc', 'abc', 'json']

    shots_files = get_all_filtered_shots("mini_film_1", state="__work", exts=extensions)
    print(type(shots_files))
    for f in shots_files:
        print(f)
