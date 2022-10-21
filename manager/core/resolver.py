from pathlib import Path

from manager import conf
from manager.core.fm import file_search
import lucidity

from manager.core.fm.file_search import pattern_format_correcter


def parse(project_name, file_pattern):
    assets_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / conf.assets_pattern_lucid
    shots_path = Path(conf.project_path_pattern) / conf.projects.get(project_name) / conf.shots_pattern_lucid

    assets_pattern = pattern_format_correcter(assets_path)
    shots_pattern = pattern_format_correcter(shots_path)

    file_pattern = pattern_format_correcter(file_pattern)

    templates = [
        lucidity.Template('shots', shots_pattern),
        lucidity.Template('rig', assets_pattern)
    ]

    data = lucidity.parse(file_pattern, templates)
    return data[0]


def get_entities(project_name, types=["*"], tasks=["*"], states=["*"], extensions=["*"]):
    entities = []
    files = file_search.get_all_filtered(project_name, types, tasks, states, extensions)
    for file in files:
        entities.append(parse(project_name, file))
    print(entities)
    return entities


if __name__ == '__main__':
    get_entities("mini_film_1")