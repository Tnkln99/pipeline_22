import lucidity
from manager import conf
from pathlib import Path
from pprint import pprint

from manager.core.resolver import parse


def get_entities(project_name="", type_req="", cat="", seq="", shot="", name="", task="", version="", name_s="",
                 state="", ext=""):
    files = get_all_filtered(project_name=project_name, type_req=type_req, cat=cat, seq=seq,
                             shot=shot, name=name, task=task, version=version, state=state, name_s=name_s, ext=ext)
    res = []
    for f in files:
        res.append(parse(project_name, f))
    return res


def get_all_filtered(project_name="", type_req="", cat="", seq="", shot="", name="", task="", version="", name_s="",
                     state="", ext=""):
    project_path = Path(conf.project_path_pattern)
    generators = []

    if type_req == "Asset":
        patternA = conf.assets_pattern_path.format(project_name=conf.projects[project_name]["name"],
                                                   cat=cat, name=name, task=task, version=version, state=state,
                                                   name_s=name_s, ext=ext)
        foundA = Path(project_path).rglob(patternA)
        generators.append(foundA)

    if type_req == "Shot":
        patternS = conf.shots_pattern_path.format(project_name=conf.projects[project_name]["name"],
                                                  seq=seq, shot=shot, task=task, version=version, state=state,
                                                  name_s=name_s, ext=ext)
        foundS = Path(project_path).rglob(patternS)
        generators.append(foundS)

    for g in generators:
        for f in g:
            yield f


def entity_to_path(data):
    templates = []

    for i in conf.lucid_patters['assets']:
        template_string = conf.lucid_patters["assets"][i]
        assets_path = Path(conf.project_path_pattern) / template_string

        assets_path = str(assets_path).replace("\\", "/")

        templates.append(lucidity.Template('assets' + i, assets_path))

    for i in conf.lucid_patters['shots']:
        template_string = conf.lucid_patters["shots"][i]
        shots_path = Path(conf.project_path_pattern) / template_string

        shots_path = str(shots_path).replace("\\", "/")

        templates.append(lucidity.Template('shots', shots_path))

    return lucidity.format(data, templates)[0]


if __name__ == '__main__':
    pprint(get_entities(project_name='mini_film_1', type_req="Asset", cat="Prop"))
    print("---------------------------------------------------------------------------------------------")
    pprint(get_entities(project_name='mini_film_1', type_req="Asset", cat="Prop", name="nice_car_01"))
    print("---------------------------------------------------------------------------------------------")
    pprint(get_entities(project_name='mini_film_1', type_req="Asset", cat="*", name="*", task="rigging"))

    print("---------------------------------------------------------------------------------------------")
    pprint(get_entities(project_name='mini_film_1', type_req="Shot", seq="*", shot="*", task="Animation"))