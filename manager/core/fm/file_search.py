from manager import conf
from pathlib import Path


def get_all_filtered(project_name, types=["*"], tasks=["*"], states=["*"], extensions=["*"]):
    project_path = Path(conf.project_path_pattern) / conf.projects.get(project_name)
    generators = []
    for type in types:
        for task in tasks:
            for state in states:
                for ext in extensions:
                    if ext == "abc":
                        pattern = conf.cache_pattern.format(type=type, task=task, ext=ext)
                    else:
                        pattern = conf.global_pattern.format(type=type, task=task, state=state, ext=ext)
                    found = Path(project_path).rglob(pattern)
                    generators.append(found)
    for g in generators:
        for f in g:
            yield f


if __name__ == '__main__':
    for i in get_all_filtered("mini_film_1"):
        print(i)
