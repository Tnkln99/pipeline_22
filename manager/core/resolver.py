from pathlib import Path

from manager import conf
import lucidity


def parse(project_name, file_pattern):
    # print(file_pattern)
    templates = []

    for i in conf.lucid_patters['assets']:
        template_string = conf.lucid_patters["assets"][i]
        assets_path = Path(conf.project_path_pattern) / conf.projects[project_name]["name"] / template_string

        assets_path = str(assets_path).replace("\\", "/")

        templates.append(lucidity.Template(i, assets_path))

    for i in conf.lucid_patters['shots']:
        template_string = conf.lucid_patters["shots"][i]
        shots_path = Path(conf.project_path_pattern) / conf.projects[project_name]["name"] / template_string

        shots_path = str(shots_path).replace("\\", "/")

        templates.append(lucidity.Template(i, shots_path))

    file_pattern = str(file_pattern).replace("\\", "/")
    data = lucidity.parse(file_pattern, templates)
    return data
