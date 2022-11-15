from manager.core.fm.file_search import get_all_filtered
from manager.core.resolver import parse
from manager.core.sg_api.connect_sg import get_from_shotgun
from pprint import pprint


def get_entities(**kwargs):
    # if we are getting data from shotgun we dont need project name.
    if "type_req" in kwargs.keys():
        entities = []
        files = get_all_filtered(**kwargs)
        for file in files:
            entities.append(parse(kwargs.get("project_name"), file))
        return entities
    # but we need shotgun type
    elif "type_req" in kwargs.keys():
        data = get_from_shotgun(**kwargs)
        return data


if __name__ == '__main__':
    pprint(get_entities(project_name='mini_film_1', cat="props"))

