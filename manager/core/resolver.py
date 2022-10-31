from pathlib import Path

from manager import conf
from manager.conf import apps
from manager.core.fm import file_search
import lucidity

from manager.core.fm.file_search import pattern_format_correcter
from pprint import pprint


def parse(project_name, file_pattern):
    assets_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / conf.lucid_patters["assets"]
    shots_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / conf.lucid_patters["shots"]
    cache_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / conf.lucid_patters["cache"]

    assets_pattern = pattern_format_correcter(assets_path)
    shots_pattern = pattern_format_correcter(shots_path)
    cache_pattern = pattern_format_correcter(cache_path)

    file_pattern = pattern_format_correcter(file_pattern)

    templates = [
        lucidity.Template('shots', shots_pattern),
        lucidity.Template('assets', assets_pattern),
        lucidity.Template('caches', cache_pattern)
    ]

    data = lucidity.parse(file_pattern, templates)
    return data


def get_entities(project_name, types=["*"], tasks=["*"], states=["*"], extensions=["*"]):
    entities = []
    files = file_search.get_all_filtered(project_name, types, tasks, states, extensions)
    for file in files:
        entities.append(parse(project_name, file))
    return entities


def entity_to_path(project_name, data):
    assets_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / conf.lucid_patters["assets"]
    shots_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / conf.lucid_patters["shots"]
    cache_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / conf.lucid_patters["cache"]

    assets_pattern = pattern_format_correcter(assets_path)
    shots_pattern = pattern_format_correcter(shots_path)
    cache_pattern = pattern_format_correcter(cache_path)

    templates = [
        lucidity.Template('caches', cache_pattern),
        lucidity.Template('shots', shots_pattern),
        lucidity.Template('assets', assets_pattern)
    ]

    return lucidity.format(data, templates)[0]


if __name__ == '__main__':

    get_entities("mini_film_1", types=[""], states=[""], extensions=apps["cache"])
