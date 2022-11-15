import lucidity
from manager import conf
from pathlib import Path
from pprint import pprint
from manager.core.resolver import parse


def get_all_filtered(project_name, cat="", seq="", shot="", name="", task="", version="", name_s="", state="", ext=""):
    project_path = Path(conf.project_path_pattern) / conf.projects.get(project_name)
    generators = []

    if cat != "":
        patternA = conf.assets_pattern_path.format(cat=cat, name=name, task=task, version=version, state=state,
                                                   name_s=name_s, ext=ext)
        print(patternA)
        foundA = Path(project_path).rglob(patternA)
        generators.append(foundA)

    if seq != "":
        patternS = conf.shots_pattern_path.format(seq=seq, shot=shot, task=task, version=version, state=state,
                                                  name_s=name_s, ext=ext)
        foundS = Path(project_path).rglob(patternS)
        generators.append(foundS)

    # patternC = conf.cache_pattern_path.format(cat=cat, name=name, task=task, version=version, ext=ext)
    # foundC = Path(project_path).rglob(patternC)
    # generators.append(foundC)

    for g in generators:
        for f in g:
            yield f


def get_entities(project_name, cat="", seq="", shot="", name="", task="", version="", name_s="", state="", ext=""):
    entities = []
    files = get_all_filtered(project_name, cat=cat, seq=seq, shot=shot, name=name, task=task,
                             version=version, name_s=name_s, state=state, ext=ext)

    for file in files:
        entities.append(parse(project_name, file))
    return entities


def entity_to_path(project_name, data):
    templates = []

    for i in conf.lucid_patters['assets']:
        template_string = conf.lucid_patters["assets"][i]
        assets_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / template_string

        assets_path = str(assets_path).replace("\\", "/")

        templates.append(lucidity.Template('assets' + i, assets_path))

    for i in conf.lucid_patters['shots']:
        template_string = conf.lucid_patters["shots"][i]
        shots_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / template_string

        shots_path = str(shots_path).replace("\\", "/")

        templates.append(lucidity.Template('shots', shots_path))

    return lucidity.format(data, templates)[0]


if __name__ == '__main__':
    pprint(
        get_entities('mini_film_1', cat="props"))

    print("---------------------------------------------------------------------------------------------")

    """files = get_all_filtered('mini_film_1', cat="*", name='*', task='*', version='*', state='*', ext='abc')
    for i in files:
        print(i)"""
